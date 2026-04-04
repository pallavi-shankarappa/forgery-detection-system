import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import os

def error_level_analysis(image_path, quality=90):
    """
    Error Level Analysis (ELA) is a technique to identify portions of an image
    that are at different compression levels. In a JPEG image, the entire
    picture should be at roughly the same error level.
    """
    # Create a temporary file path for the resaved image
    temp_path = f"temp_resaved_{os.path.basename(image_path)}"
    
    try:
        # Load the original image
        original = Image.open(image_path).convert('RGB')
        
        # Save as JPEG with the specified quality
        original.save(temp_path, 'JPEG', quality=quality)
        resaved = Image.open(temp_path)
        
        # Calculate the absolute difference between original and resaved
        diff = ImageChops.difference(original, resaved)
        
        # Enhance the difference to make it visible
        extrema = diff.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        if max_diff == 0:
            max_diff = 1
        scale = 255.0 / max_diff
        
        ela_image = ImageEnhance.Brightness(diff).enhance(scale)
        
        # Save the ELA image
        ela_filename = f"ela_{os.path.basename(image_path)}"
        ela_path = os.path.join(os.path.dirname(image_path), ela_filename)
        ela_image.save(ela_path)
        
        # Calculate a basic confidence score based on the difference
        # High variation in ELA often indicates potential manipulation
        diff_np = np.array(diff)
        mean_diff = np.mean(diff_np)
        std_diff = np.std(diff_np)
        
        # Normalize score (this is a heuristic, real models are more complex)
        score = min(100, max(0, (mean_diff * 10) + (std_diff * 2)))
        
        return ela_path, round(score, 2)
    
    finally:
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

def analyze_metadata(image_path):
    """
    Simple metadata check for manipulation markers.
    """
    try:
        img = Image.open(image_path)
        info = img.info
        
        suspicious_tags = ['Adobe Photoshop', 'GIMP', 'Pixlr', 'Canva']
        markers_found = []
        
        for tag, value in info.items():
            for susp in suspicious_tags:
                if susp.lower() in str(value).lower():
                    markers_found.append(susp)
                    
        return markers_found
    except Exception:
        return []

def detect_forgery(image_path):
    """
    Main entry point for forgery detection.
    Combines ELA, metadata, and heuristic analysis.
    """
    ela_path, ela_score = error_level_analysis(image_path)
    metadata_markers = analyze_metadata(image_path)
    
    # Final decision logic
    final_score = ela_score
    if metadata_markers:
        final_score = min(100, final_score + 20)
        
    is_forged = final_score > 50
    
    result = {
        "is_forged": bool(is_forged),
        "confidence_score": final_score,
        "ela_image": os.path.basename(ela_path),
        "metadata_markers": metadata_markers,
        "analysis_summary": f"Detected potential forgery with {final_score}% confidence." if is_forged else "No significant forgery detected."
    }
    
    return result
