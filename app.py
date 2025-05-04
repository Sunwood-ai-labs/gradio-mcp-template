import numpy as np
import gradio as gr
import qrcode
from PIL import Image
import io  # Added for parity with user-provided snippet (currently unused)


def reverse_text(text):
    """
    テキストを反転する。

    Args:
        text (str): 反転したいテキスト。

    Returns:
        str: 反転されたテキスト。
    """
    return text[::-1]


def generate_qr_code(text):
    """
    テキストからQRコードを生成する。

    Args:
        text (str): QRコードに埋め込むテキスト。

    Returns:
        numpy.ndarray: 生成されたQRコード画像 (RGB)。
    """
    qr = qrcode.QRCode(version=5, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # PILイメージをNumPy配列に変換
    img_array = np.array(img.convert("RGB"))
    return img_array


def count_words(text):
    """
    テキストの単語数をカウントする。

    Args:
        text (str): カウントしたいテキスト。

    Returns:
        int: 単語数。
    """
    if not text.strip():
        return 0
    return len(text.split())


def resize_image(image, width, height):
    """
    画像をリサイズする。

    Args:
        image (numpy.ndarray): リサイズしたい画像。
        width (int): 新しい幅。
        height (int): 新しい高さ。

    Returns:
        numpy.ndarray: リサイズされた画像 (RGB)。
    """
    # NumPy配列からPILイメージに変換
    pil_image = Image.fromarray(image)

    resized_image = pil_image.resize((int(width), int(height)))
    return np.array(resized_image)


# --- Interface -----------------------------------------------------------

resize_interface = gr.Interface(
    fn=resize_image,
    inputs=[
        gr.Image(),
        gr.Number(label="幅", value=300),
        gr.Number(label="高さ", value=300),
    ],
    outputs=gr.Image(),
    api_name="resize_image",
)


demo = gr.TabbedInterface(
    [
        gr.Interface(reverse_text, gr.Textbox(), gr.Textbox(), api_name="reverse_text"),
        gr.Interface(generate_qr_code, gr.Textbox(), gr.Image(), api_name="generate_qr_code"),
        gr.Interface(count_words, gr.Textbox(), gr.Number(), api_name="count_words"),
        resize_interface,
    ],
    [
        "テキスト反転",
        "QRコード生成",
        "単語数カウント",
        "画像リサイズ",
    ],
)


if __name__ == "__main__":
    # mcp_server=True starts the SSE endpoint at /gradio_api/mcp/sse
    demo.launch(mcp_server=True)
