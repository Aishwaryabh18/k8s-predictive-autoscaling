import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

WINDOW = 10

class LSTMModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(3, 32, batch_first=True)
        self.fc = nn.Linear(32, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

# Load CSV
df = pd.read_csv("metrics.csv")
data = df.values

scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

X, y = [], []
for i in range(len(data_scaled) - WINDOW):
    X.append(data_scaled[i:i+WINDOW])
    y.append(data_scaled[i+WINDOW][0])  # predict future CPU

X = torch.tensor(np.array(X)).float()
y = torch.tensor(np.array(y)).float().unsqueeze(1)

model = LSTMModel()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(50):
    optimizer.zero_grad()
    output = model(X)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch}, Loss: {loss.item()}")

torch.save(model.state_dict(), "lstm.pt")