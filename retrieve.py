import argparse
import torch
from datasets import load_dataset
from torch.utils.data import DataLoader
from model import D2SModel
from tqdm import tqdm
parser = argparse.ArgumentParser(description="LSR Index Pisa")
parser.add_argument("--data", type=str,
                    default="lsr42/mscoco-blip-dense")
parser.add_argument("--batch_size", type=int,
                    default=1024, help="eval batch size")
parser.add_argument(
    "--model", type="str", default="lsr42/d2s_mscoco-blip-dense_q_reg_0.001_d_reg_0.001")
args = parser.parse_args()
device = "cuda:0" if torch.cuda.is_available() else "cpu"
dataset = load_dataset(args.data, data_files={"img_emb": "img_embs.parquet",
                                              "text_emb": "text_embs.parquet"}, keep_in_memory=True).with_format("torch")
img_dataloader = DataLoader(dataset["img_emb"], batch_size=args.batch_size)
model = D2SModel.from_pretrained(args.model).to(device)

for batch in tqdm(img_dataloader, desc="Encode images"):
    batch_ids = batch["id"]
    batch_dense = batch["emb"].to(device)
    batch_sparse = model(batch_dense)
