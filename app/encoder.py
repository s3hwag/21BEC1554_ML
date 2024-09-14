from sentence_transformers import SentenceTransformer
import numpy as np

# Load a pre-trained SentenceTransformer model
model_name = 'all-MiniLM-L6-v2'  # You can choose a different model if needed
model = SentenceTransformer(model_name)

def encode_text(text: str) -> np.ndarray:
    """
    Encode a given text into a vector embedding using the pre-trained model.
    
    Args:
        text (str): The input text to encode.

    Returns:
        np.ndarray: The vector embedding of the input text.
    """
    # Generate the embedding for the input text
    embedding = model.encode(text)
    
    return embedding


if __name__ == "__main__":
    sample_text = "Document retrieval systems are essential for modern search applications."
    embedding = encode_text(sample_text)
    print(f"Embedding for the sample text:\n{embedding}")
