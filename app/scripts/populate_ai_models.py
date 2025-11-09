"""
Script to populate the database with some example AI models
Run with: python -m app.scripts.populate_ai_models
"""
from app.database import SessionLocal
from app.repositories import AIModelRepository
from app.api.schemas import AIModelCreate


def create_sample_models():
    """Create sample AI models in the database"""
    db = SessionLocal()
    repository = AIModelRepository(db)
    
    sample_models = [
        AIModelCreate(
            name="GPT-4",
            provider="openai",
            model_id="gpt-4",
            model_type="chat",
            description="GPT-4 is a large-scale, multimodal model which can accept image and text inputs and produce text outputs.",
            max_tokens=4096,
            input_cost_per_token=0.00003,
            output_cost_per_token=0.00006,
            context_window=8192,
            is_active=True
        ),
        AIModelCreate(
            name="GPT-3.5 Turbo",
            provider="openai",
            model_id="gpt-3.5-turbo",
            model_type="chat",
            description="GPT-3.5 Turbo is optimized for chat at 1/10th the cost of text-davinci-003.",
            max_tokens=4096,
            input_cost_per_token=0.0000015,
            output_cost_per_token=0.000002,
            context_window=4096,
            is_active=True
        ),
        AIModelCreate(
            name="Claude-3 Sonnet",
            provider="anthropic",
            model_id="claude-3-sonnet-20240229",
            model_type="chat",
            description="Claude-3 Sonnet strikes the ideal balance between intelligence and speed for enterprise workloads.",
            max_tokens=4096,
            input_cost_per_token=0.000003,
            output_cost_per_token=0.000015,
            context_window=200000,
            is_active=True
        ),
        AIModelCreate(
            name="Text Embedding Ada 002",
            provider="openai",
            model_id="text-embedding-ada-002",
            model_type="embedding",
            description="OpenAI's text-embedding-ada-002 model for creating embeddings.",
            max_tokens=8191,
            input_cost_per_token=0.0000001,
            output_cost_per_token=0.0,
            context_window=8191,
            is_active=True
        ),
        AIModelCreate(
            name="Command R+",
            provider="cohere",
            model_id="command-r-plus",
            model_type="chat",
            description="Command R+ is Cohere's flagship text generation model optimized for conversational interaction and long context tasks.",
            max_tokens=4096,
            input_cost_per_token=0.000003,
            output_cost_per_token=0.000015,
            context_window=128000,
            is_active=True
        )
    ]
    
    created_models = []
    for model_data in sample_models:
        try:
            # Check if model already exists
            existing = repository.get_by_model_id(model_data.model_id, model_data.provider)
            if not existing:
                model = repository.create(model_data)
                created_models.append(model)
                print(f"Created: {model.name} ({model.provider})")
            else:
                print(f"Skipped: {model_data.name} ({model_data.provider}) - already exists")
        except Exception as e:
            print(f"Error creating {model_data.name}: {e}")
    
    db.close()
    print(f"\nSuccessfully created {len(created_models)} AI models")
    return created_models


if __name__ == "__main__":
    create_sample_models()