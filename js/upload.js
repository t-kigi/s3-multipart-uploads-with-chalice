import axios from "axios";

const FILE_CHUNK_SIZE = 100 * 1024 * 1024; // 分割単位: 本番: 100MB, テスト時 5MB

function getExt(filename) {
  var idx = filename.lastIndexOf(".");
  if (idx >= 0) {
    return filename.slice(idx + 1);
  }
  return "";
}

// パートデータの読み出し用 Promise を返す
function readPartData(index, fileBlob) {
  return new Promise((resolve, reject) => {
    var reader = new FileReader();
    var offset = index * FILE_CHUNK_SIZE;

    reader.onload = function (e) {
      var data = new Uint8Array(e.target.result);
      resolve({
        index: index,
        data: data,
      });
      reader.abort();
    };

    var slice = fileBlob.slice(offset, offset + FILE_CHUNK_SIZE, fileBlob.type);

    reader.readAsArrayBuffer(slice);
  });
}

async function upload(e) {
  // アップロードするファイルを選択した時点で開始
  const filedata = e.currentTarget.files[0];
  if (!filedata) {
    alert("ファイルが指定されていません。");
    return;
  }
  // この個数分ファイルをアップロードする
  const totalPartNumber = Math.ceil(filedata.size / FILE_CHUNK_SIZE);
  let url = "/api/multipart_upload/start";
  const ext = getExt(filedata.name);
  if (ext) {
    url = url + "/" + ext;
  }

  const { data } = await axios.put(url, { TotalPart: totalPartNumber });

  const key = data.UploadKey;
  const uploadId = data.UploadId;
  const totalPartCount = data.Parts.length;

  let completed = 0;
  const updateProgress = () => {
    // 進捗バー更新
    var progress = parseInt((completed / totalPartNumber) * 10000) / 100;
    var width = Math.round(progress);
    var bar = document.querySelector("#upload-status .progress-bar");
    bar.textContent = "" + progress + "%";
    bar.style.width = "" + width + "%";
    bar.setAttribute("aria-valuenow", width);
    var msg = document.querySelector("#upload-status .progress-message");
    var fsize = parseInt((filedata.size / 1024 / 1024) * 100) / 100;
    msg.innerText = `ファイルサイズ: ${fsize} MB, アップロード完了パート数: ${completed} / ${totalPartCount}`;
  };
  // 表示初期化
  updateProgress();

  const partUploads = data.Parts.map((part, index) => {
    return () => {
      return readPartData(index, filedata).then(async (partdata) => {
        const content = partdata.data;
        const uploadUrl = part.url;
        // アップロード開始
        const res = await axios.put(uploadUrl, content, {
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Expose-Headers": "etag",
            "Content-Type": "", // no content-type required
          },
        });

        // アップロード完了
        // 完了通知に必要な情報を作成して返す
        return {
          ETag: res.headers.etag.replaceAll('"', ""),
          PartNumber: data.Parts[index].part,
        };
      });
    };
  });

  // 順次実行して解決
  // await をかけずに大量の平行アップロードすることも可能だが、
  // 本数が多い場合ブラウザで CPU ビジーとなるため、ここでは効率が悪いが１本ずつアップロードしている
  let uploadedParts = [];
  for (const part of partUploads) {
    const uploaded = await part();
    completed++;
    updateProgress();
    uploadedParts = uploadedParts.concat([uploaded]);
  }

  // 全て完了まで待機して順次処理
  const completeUrl = "/api/multipart_upload/complete";
  await axios.put(completeUrl, {
    Key: key,
    Parts: uploadedParts,
    UploadId: uploadId,
  });
  const bar = document.querySelector("#upload-status .progress-bar");
  bar.textContent = "アップロードが完了しました。";
}

document.addEventListener(
  "DOMContentLoaded",
  () => {
    const uploaded = document.querySelector("#form2uploadedfile");
    if (!uploaded) return;
    uploaded.addEventListener("change", upload);
  },
  false
);
