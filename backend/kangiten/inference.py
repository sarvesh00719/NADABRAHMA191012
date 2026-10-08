import torch
from torch.nn import functional as F
from model import KangitenModel
from data import DummyTokenizer

class KangitenInference:
    def __init__(self, checkpoint_path: str = "kangiten_checkpoint.pt", device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = DummyTokenizer()
        self.model = KangitenModel(vocab_size=self.tokenizer.vocab_size).to(self.device)
        
        try:
            self.model.load_state_dict(torch.load(checkpoint_path, map_location=self.device))
            print(f"Loaded checkpoint from {checkpoint_path}")
        except FileNotFoundError:
            print("No checkpoint found. Using randomly initialized weights.")
            
        self.model.eval()
        
    def generate(self, prompt: str, max_new_tokens: int = 50, temperature: float = 0.8) -> str:
        idx = torch.tensor([self.tokenizer.encode(prompt)], dtype=torch.long).to(self.device)
        
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -1024:]
            
            with torch.no_grad():
                logits, _ = self.model(idx_cond)
                
            logits = logits[:, -1, :] / temperature
            probs = F.softmax(logits, dim=-1)
            
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)
            
            if idx_next.item() == self.tokenizer.eos_token_id:
                break
                
        out_tokens = idx[0].tolist()
        return self.tokenizer.decode(out_tokens)

if __name__ == "__main__":
    infer = KangitenInference()
    print("User: I feel stressed.")
    print("Kangiten:", infer.generate("User: I feel stressed.\\nAssistant:"))
