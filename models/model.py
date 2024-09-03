import torch
import torch.nn.functional as F
from torch_geometric.nn import GATConv
from torch_geometric.data import Data

# GATNet 모델 정의
class GATNet(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, heads=8, dropout=0.2):
        super(GATNet, self).__init__()
        self.gat1 = GATConv(input_dim, hidden_dim, heads=heads, concat=True, dropout=dropout)
        self.gat2 = GATConv(hidden_dim * heads, output_dim, heads=1, concat=False, dropout=dropout)
        self.dropout = torch.nn.Dropout(dropout)
        self.batch_norm1 = torch.nn.BatchNorm1d(hidden_dim * heads)  # 배치 정규화 추가

    def forward(self, x, edge_index):
        x = self.gat1(x, edge_index)
        x = self.batch_norm1(x)  # 배치 정규화
        x = F.elu(x)
        x = self.dropout(x)
        x = self.gat2(x, edge_index)
        return x

input_dim = x_train.size(1)
hidden_dim = 128  # 히든 차원 확장
output_dim = input_dim

model = GATNet(input_dim, hidden_dim, output_dim, heads=8, dropout=0.3).to(device)  # 드롭아웃 증가
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=5e-4)  # 학습률 감소, weight_decay 증가
criterion = torch.nn.MSELoss()

model.train()
for epoch in range(1, 5001):  
    optimizer.zero_grad()
    out = model(data_train.x, data_train.edge_index)
    loss = criterion(out, data_train.x)
    loss.backward()
    optimizer.step()
    
    if epoch % 100 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item():.4f}')
