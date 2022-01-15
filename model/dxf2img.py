import ezdxf
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend


# Credits: https://github.com/Hamza442004/DXF2img
class dxf2img:
    def __init__(self):
        pass

    def convert(self, dxf_file, out_file, background_color="#FFFFFF", img_res=300) -> bool:
        doc = ezdxf.readfile(dxf_file)
        msp = doc.modelspace()

        # Recommended: audit & repair DXF document before rendering
        auditor = doc.audit()
        # The auditor.errors attribute stores severe errors,
        # which *may* raise exceptions when rendering.
        if len(auditor.errors) != 0:
            raise Exception("This DXF document is damaged and can't be converted! --> ", dxf_file)

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc)
        ctx.set_current_layout(msp)
        ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = background_color
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(msp, finalize=True)

        fig.savefig(out_file, dpi=img_res)
        print(dxf_file, " Converted Successfully")


# if __name__ == "__main__":
#     dxf2img().convert("C:/Users/65844/Desktop/citrus/floorplan/depot.dxf", "C:/Users/65844/Desktop/out")
