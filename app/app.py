import re, torch, gradio as gr
from transformers import T5Tokenizer, MT5ForConditionalGeneration

MT5 = r"C:\Users\aipmu\OneDrive\Desktop\Absa\third_party\M-ABSA\eval_baseline_mT5\mT5-base"
CKPT = {
    "Joint model (en+de+ru+zh, 8 epochs)": r"D:\absa_backup_joint_ep8\cktepoch=30.ckpt",
    "English-only model (30 epochs)": r"C:\Users\aipmu\OneDrive\Desktop\Absa\outputs\checkpoints\restaurant_en_ep30\cktepoch=30.ckpt",
    "German-only model (supervised)": r"D:\absa_backup_de_ep30\cktepoch=30.ckpt",
}
T = re.compile(r"\((.*?), ([^,()]*), (positive|negative|neutral)\)")
dev = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
tok = T5Tokenizer.from_pretrained(MT5)
cache = {"name": None, "model": None}

def load(name):
    if cache["name"] != name:
        cache["model"] = None
        if dev.type == "cuda":
            torch.cuda.empty_cache()
        m = MT5ForConditionalGeneration.from_pretrained(MT5)
        sd = torch.load(CKPT[name], map_location="cpu")["state_dict"]
        sd = {k[len("model."):]: v for k, v in sd.items() if k.startswith("model.")}
        print("load_state_dict:", m.load_state_dict(sd, strict=False))
        cache["model"] = m.to(dev).eval()
        cache["name"] = name
    return cache["model"]

def run(review, name):
    if not review or not review.strip():
        return [], ""
    m = load(name)
    text = " ".join(re.sub(r"([.,!?;:()])", r" \1 ", review).split())
    enc = tok.batch_encode_plus([text], max_length=128, padding="max_length", truncation=True, return_tensors="pt")
    with torch.no_grad():
        out = m.generate(input_ids=enc["input_ids"].to(dev), attention_mask=enc["attention_mask"].to(dev), max_length=128)
    raw = tok.decode(out[0], skip_special_tokens=True)
    rows, seen = [], set()
    for a, c, p in T.findall(raw):
        t = (a.strip(), c.strip(), p)
        if t not in seen:
            seen.add(t)
            rows.append(list(t))
    return rows, raw

demo = gr.Interface(
    fn=run,
    inputs=[gr.Textbox(lines=3, label="Restaurant review (any of the 21 languages)"),
            gr.Dropdown(list(CKPT), value=list(CKPT)[0], label="Model")],
    outputs=[gr.Dataframe(headers=["aspect term", "category", "sentiment"], label="Extracted triplets"),
             gr.Textbox(label="Raw model output")],
    title="M-ABSA: multilingual aspect-based sentiment (Restaurant, TASD)",
    allow_flagging="never")

if __name__ == "__main__":
    demo.launch(inbrowser=True)
