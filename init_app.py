import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import nilearn
    from nilearn import datasets
    from ipyniivue import NiiVue
    from pathlib import Path

    return NiiVue, Path, datasets, mo


@app.cell
def _():
    import nibabel as nib

    return (nib,)


@app.cell
def _(datasets):
    fsaverage = datasets.fetch_surf_fsaverage(mesh="fsaverage")
    fsaverage
    return (fsaverage,)


@app.cell
def _(nib):
    import numpy as np

    def annot_to_label_gii(annot_path, out_path):
        labels, ctab, names = nib.freesurfer.read_annot(annot_path)
    
        label_table = nib.gifti.GiftiLabelTable()
        for i, (name, color) in enumerate(zip(names, ctab)):
            gl = nib.gifti.GiftiLabel(
                key=i,
                red=color[0]/255,
                green=color[1]/255,
                blue=color[2]/255,
                alpha=1.0
            )
            gl.label = name.decode() if isinstance(name, bytes) else name
            label_table.labels.append(gl)

        arr = nib.gifti.GiftiDataArray(
            data=labels.astype(np.int32),
            intent=nib.nifti1.intent_codes['NIFTI_INTENT_LABEL'],
            datatype='NIFTI_TYPE_INT32'
        )
        img = nib.gifti.GiftiImage(darrays=[arr], labeltable=label_table)
        nib.save(img, out_path)

    annot_to_label_gii("data/atlases/lh.HCPMMP1.annot", "data/atlases/lh.HCPMMP1.label.gii")
    annot_to_label_gii("data/atlases/rh.HCPMMP1.annot", "data/atlases/rh.HCPMMP1.label.gii")
    return


@app.cell
def _():
    """

    nv = NiiVue()
    nv.load_meshes([
        {"path": Path(fsaverage["infl_left"]), "rgba255": [64, 22, 222, 255]}, {"path": Path(fsaverage["infl_right"]), "rgba255": [222, 64, 22, 255]}
    ]) 
    nv

    """
    """
    nv = NiiVue()
    nv.load_meshes([
        {
            "path": Path(fsaverage["infl_left"]),
            "layers": [{"path": Path("data/atlases/lh.HCPMMP1.label.gii")}]
        },
        {
            "path": Path(fsaverage["infl_right"]),
            "layers": [{"path": Path("data/atlases/rh.HCPMMP1.label.gii")}]
        },
    ])
    nv
    """
    return


@app.cell
def _(fsaverage):
    from nilearn import plotting

    plotting.plot_surf_roi(
        surf_mesh=fsaverage["infl_left"],
        roi_map="data/atlases/lh.HCPMMP1.annot",
        hemi="left",
        view="lateral",
        bg_map=fsaverage["sulc_left"],
    )
    return


@app.cell
def _(mo):
    hemi = mo.ui.radio(
        options=["Left", "Right", "Both"],
        value="Both",
        label="Hemisphere"
    )
    hemi
    return (hemi,)


@app.cell
def _(mo):
    get_label, set_label = mo.state("Hover over brain...")
    return get_label, set_label


@app.cell
def _():
    return


@app.cell
def _(NiiVue, Path, fsaverage, hemi, set_label):
    meshes = []
    if hemi.value in ("Left", "Both"):
        meshes.append({
            "path": Path(fsaverage["infl_left"]),
            "layers": [{"path": Path("data/atlases/lh.HCPMMP1.label.gii")}]
        })
    if hemi.value in ("Right", "Both"):
        meshes.append({
            "path": Path(fsaverage["infl_right"]),
            "layers": [{"path": Path("data/atlases/rh.HCPMMP1.label.gii")}]
        })

    nv = NiiVue()
    nv.load_meshes(meshes)


    @nv.on_location_change
    def show_location(location):
        set_label(location["string"])

    nv
    return


@app.cell
def _(get_label, mo):

    mo.md(get_label())
    return


if __name__ == "__main__":
    app.run()
