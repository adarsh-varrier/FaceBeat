from transformers import pipeline

# Initialize the emotion detection model
emotion_classifier = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base', return_all_scores=True)

def detect_emotion(text):
    """
    Detects the most relevant emotion from the input text using the transformer model.
    Args:
        text (str): Input text from the user.
    Returns:
        str: Detected emotion label.
    """
    # Define specific keywords for romance
    romance_keywords = ["love", "in love", "crush", "adore", "sweetheart", "romantic"]

    # Check if any romance-specific keywords are in the input text
    if any(keyword in text.lower() for keyword in romance_keywords):
        return "romance"
    # Get predictions from the emotion classifier
    predictions = emotion_classifier(text)
    
    # Extract the highest-scored emotion
    highest_emotion = max(predictions[0], key=lambda x: x['score'])['label']
    
    # Map detected emotion to moods in the model
    emotion_to_mood = {
        'admiration': 'overjoyed',
        'adoration': 'romance',
        'amusement': 'happy',
        'anger': 'anger',
        'anxiety': 'relax',
        'awe': 'relax',
        'awkwardness': 'relax',
        'boredom': 'nostalgia',
        'calmness': 'relax',
        'confusion': 'interest',
        'craving': 'satisfaction',
        'disgust': 'sad',
        'empathic pain': 'sad',
        'entrancement': 'excitement',
        'excitement': 'excitement',
        'fear': 'fear',
        'happiness': 'happy',
        'interest': 'interest',
        'joy': 'happy',
        'nostalgia': 'nostalgia',
        'relief': 'relax',
        'romance': 'romance',
        'sadness': 'sad',
        'satisfaction': 'satisfaction',
        'surprise': 'surprise',
    }
    
    # Return the corresponding mood or a default
    return emotion_to_mood.get(highest_emotion, 'relax')
