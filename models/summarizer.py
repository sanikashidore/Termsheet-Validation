"""
Summarization module - generates a summary of term sheet content
"""
import re

def generate_summary(text):
    """
    Generates a summary of term sheet content
    
    Args:
        text (str): The term sheet text
        
    Returns:
        str: Generated summary
    """
    # For a lightweight approach, we'll use extractive summarization
    # by identifying key sections and sentences
    
    # Extract key parts based on common term sheet sections
    key_sections = [
        'parties', 'financing', 'amount', 'valuation', 'price', 
        'rights', 'conditions', 'closing', 'governance'
    ]
    
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Score sentences based on keyword presence and position
    scored_sentences = []
    for i, sentence in enumerate(sentences):
        score = 0
        
        # Position score - sentences at the beginning often contain key information
        position_score = max(0, 1.0 - (i / len(sentences)))
        score += position_score * 0.3
        
        # Keyword score
        for section in key_sections:
            if re.search(r'\b' + section + r'\b', sentence, re.IGNORECASE):
                score += 0.5
        
        # Length penalty - avoid very short sentences
        if len(sentence.split()) < 5:
            score -= 0.2
        
        # Prioritize sentences with numbers (often key terms)
        if re.search(r'\d', sentence):
            score += 0.3
            
        # Additional score for sentences containing monetary values
        if re.search(r'[$€£¥]\s*\d+', sentence):
            score += 0.4
        
        scored_sentences.append((sentence, score))
    
    # Sort sentences by score and select top ones
    top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:5]
    
    # Sort selected sentences back in original order
    summary_sentences = sorted(
        [(sentences.index(sentence), sentence) for sentence, score in top_sentences]
    )
    
    # Combine sentences into a summary
    summary = " ".join(sentence for _, sentence in summary_sentences)
    
    # Add fallback if summary is too short
    if len(summary.split()) < 20:
        first_sentences = " ".join(sentences[:3])
        if len(summary) > 0:
            summary = summary + " " + first_sentences
        else:
            summary = first_sentences
    
    return summary