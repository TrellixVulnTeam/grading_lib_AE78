import os
import tarfile
import zipfile
from shutil import copyfile


def extract_moodle_zip(zippath, outpath, tmpdir, roster, internal_tarball=True):
    zipdir = os.path.join(tmpdir, "zip")
    with zipfile.ZipFile(zippath) as zf:
        zf.extractall(zipdir)

    subdirs = os.listdir(zipdir)

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    for sdir in subdirs:
        name = sdir.split("_")[0]
        fname, lname = name.split(" ")

        sid = roster.get_student_id_by_name(fname, lname)

        assert sid is not None, "Unknown student"

        if internal_tarball:
            # TODO: catch exceptions and give good error.
            tarball_name = os.listdir(os.path.join(zipdir, sdir))[0]
            tarpath = os.path.join(zipdir, sdir, tarball_name)

            if not tarpath.endswith(".tar.gz"):
                print("Student submission must be a tar.gz. filename was {}".format(tarpath))
                continue
            sopath = os.path.join(outpath, sid)
            try:
                with tarfile.open(tarpath, mode="r:gz") as tf:
                    tf.extractall(sopath)
            except tarfile.ReadError:
                print("Submission was not a valid tarball.")
            print(sid)
        else:
            submission_name = os.listdir(os.path.join(zipdir, sdir))[0]
            submissionpath = os.path.join(zipdir, sdir, submission_name)

            ext = ""
            if "." in submission_name:
                ext = submission_name[submission_name.index("."):]
            new_path = os.path.join(outpath, sid + ext)

            copyfile(submissionpath, new_path)
