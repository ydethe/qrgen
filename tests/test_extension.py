from qrgen.server import generate_qrcode


def test_qrcode_generation():
    generate_qrcode(
        code_size=10,
        correction="m",
        code_data="foo",
        back_color=(255, 255, 255),
        fill_color=(0, 0, 0),
        style="SquareModuleDrawer",
    )


if __name__ == "__main__":

    test_qrcode_generation()
