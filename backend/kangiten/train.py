import torch
import torch.optim as optim
from model import KangitenModel
from data import DummyTokenizer

def train_skeleton():
    print("Initializing Kangiten training skeleton...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Hyperparams
    vocab_size = 50000
    batch_size = 4
    seq_len = 64
    epochs = 1
    
    model = KangitenModel(vocab_size=vocab_size).to(device)
    optimizer = optim.AdamW(model.parameters(), lr=3e-4)
    
    print("Starting training loop...")
    for epoch in range(epochs):
        x = torch.randint(0, vocab_size, (batch_size, seq_len)).to(device)
        y = torch.randint(0, vocab_size, (batch_size, seq_len)).to(device)
        
        logits, loss = model(x, targets=y)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")
        
    print("Training complete. Saving checkpoint...")
    torch.save(model.state_dict(), "kangiten_checkpoint.pt")
    print("Saved kangiten_checkpoint.pt")

if __name__ == "__main__":
    train_skeleton()
