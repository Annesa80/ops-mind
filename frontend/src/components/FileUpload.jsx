import { useRef, useState } from "react";

function FileUpload() {

  const [isOpen, setIsOpen] = useState(false);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  const fileInputRef = useRef(null);


  function openModal() {

    setMessage("");
    setFile(null);
    setIsOpen(true);

  }


  function closeModal() {

    if (uploading) return;

    setIsOpen(false);
    setFile(null);
    setMessage("");

  }


  function handleFileChange(event) {

    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);
    setMessage("");

  }


  async function handleUpload() {

    if (!file) {
      setMessage("Please choose a file first.");
      return;
    }


    setUploading(true);
    setMessage("");


    const formData = new FormData();

    formData.append("file", file);


    try {

      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData
        }
      );


      const data = await response.json();


      if (!response.ok || data.error) {

        throw new Error(
          data.error || "Upload failed."
        );

      }


      /*
       * Upload succeeded.
       *
       * Show success message first.
       */

      setMessage(
        `✓ ${data.filename} added successfully (${data.chunks_added} chunks)`
      );


      /*
       * Remove the selected file from the UI.
       */

      setFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }


      /*
       * Automatically close the popup
       * after a short delay.
       */

      setTimeout(() => {

        setIsOpen(false);
        setMessage("");

      }, 1800);


    } catch (error) {

      console.error(error);

      setMessage(
        `✕ ${error.message}`
      );

    } finally {

      setUploading(false);

    }

  }


  return (

    <>

      {/* Upload button */}

      <button
        onClick={openModal}
        className="
          px-4
          py-2
          rounded-lg
          border
          border-slate-300
          bg-white
          text-slate-700
          text-sm
          font-medium
          hover:bg-slate-50
          transition
          flex
          items-center
          gap-2
        "
      >
        📎 Upload
      </button>


      {/* Modal */}

      {isOpen && (

        <div
          className="
            fixed
            inset-0
            z-50
            flex
            items-center
            justify-center
            bg-black/40
            px-4
          "
          onClick={closeModal}
        >

          <div
            className="
              w-full
              max-w-md
              rounded-2xl
              bg-white
              shadow-2xl
              p-6
            "
            onClick={(event) => event.stopPropagation()}
          >

            {/* Header */}

            <div className="flex items-center justify-between mb-5">

              <div>

                <h2 className="text-xl font-semibold text-slate-900">
                  Upload Knowledge
                </h2>

                <p className="text-sm text-slate-500 mt-1">
                  Add a document to OpsMind's knowledge base.
                </p>

              </div>


              <button
                onClick={closeModal}
                disabled={uploading}
                className="
                  text-slate-400
                  hover:text-slate-700
                  text-xl
                  disabled:opacity-40
                "
              >
                ✕
              </button>

            </div>


            {/* File selector */}

            <label
              className="
                block
                border-2
                border-dashed
                border-slate-300
                rounded-xl
                p-6
                text-center
                cursor-pointer
                hover:border-blue-400
                hover:bg-blue-50/30
                transition
              "
            >

              <div className="text-3xl mb-2">
                📄
              </div>

              <p className="font-medium text-slate-700">
                Choose a file
              </p>

              <p className="text-xs text-slate-400 mt-1">
                Markdown, TXT, PDF, or DOCX
              </p>


              <input
                ref={fileInputRef}
                type="file"
                accept=".md,.txt,.pdf,.docx"
                onChange={handleFileChange}
                className="hidden"
              />

            </label>


            {/* Selected file */}

            {file && (

              <div
                className="
                  mt-4
                  flex
                  items-center
                  gap-3
                  bg-slate-50
                  border
                  border-slate-200
                  rounded-lg
                  p-3
                "
              >

                <span className="text-xl">
                  📄
                </span>

                <div className="min-w-0 flex-1">

                  <p className="text-sm font-medium text-slate-700 truncate">
                    {file.name}
                  </p>

                  <p className="text-xs text-slate-400">
                    {(file.size / 1024).toFixed(1)} KB
                  </p>

                </div>


                {!uploading && (

                  <button
                    onClick={() => {
                      setFile(null);

                      if (fileInputRef.current) {
                        fileInputRef.current.value = "";
                      }
                    }}
                    className="text-slate-400 hover:text-red-500"
                  >
                    ✕
                  </button>

                )}

              </div>

            )}


            {/* Confirmation */}

            {file && !message && (

              <p className="text-sm text-slate-500 mt-4">
                Ready to add <strong>{file.name}</strong> to the
                OpsMind knowledge base?
              </p>

            )}


            {/* Status message */}

            {message && (

              <div
                className={`
                  mt-4
                  rounded-lg
                  px-4
                  py-3
                  text-sm
                  ${
                    message.startsWith("✓")
                      ? "bg-green-50 text-green-700 border border-green-200"
                      : message.startsWith("✕")
                        ? "bg-red-50 text-red-700 border border-red-200"
                        : "bg-slate-50 text-slate-600"
                  }
                `}
              >
                {message}
              </div>

            )}


            {/* Actions */}

            <div className="flex justify-end gap-3 mt-6">

              <button
                onClick={closeModal}
                disabled={uploading}
                className="
                  px-4
                  py-2
                  rounded-lg
                  border
                  border-slate-300
                  text-slate-600
                  text-sm
                  font-medium
                  hover:bg-slate-50
                  disabled:opacity-50
                "
              >
                Cancel
              </button>


              <button
                onClick={handleUpload}
                disabled={!file || uploading}
                className="
                  px-5
                  py-2
                  rounded-lg
                  bg-blue-600
                  text-white
                  text-sm
                  font-medium
                  hover:bg-blue-700
                  disabled:bg-slate-300
                  disabled:cursor-not-allowed
                "
              >

                {uploading
                  ? "Adding..."
                  : "Add to Knowledge Base"}

              </button>

            </div>

          </div>

        </div>

      )}

    </>

  );

}

export default FileUpload;