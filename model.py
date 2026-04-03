import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import RobertaModel

class LightweightModel(nn.Module):
    def __init__(self, model_name="microsoft/codebert-base", proj_dim=128):
        super().__init__()
        self.bert = RobertaModel.from_pretrained(model_name)
        self.projector = nn.Linear(self.bert.config.hidden_size, proj_dim)

    def encode(self, ids, mask):
        h = self.bert(ids, mask).last_hidden_state[:, 0, :]
        p = self.projector(h)
        return F.normalize(p, dim=-1)

    def forward(self, ids, mask):
        return self.encode(ids, mask)
