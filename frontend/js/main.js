const API_BASE_URL = "http://127.0.0.1:5000";

const zh = (text) => JSON.parse(`"${text}"`);

const textMap = {
    pageTitle: zh("\\u0052\\u0065\\u0061\\u006c\\u002d\\u0045\\u0053\\u0052\\u0047\\u0041\\u004e \\u56fe\\u50cf\\u8d85\\u5206\\u8fa8\\u7387\\u589e\\u5f3a\\u7cfb\\u7edf"),
    heroTag: zh("\\u8bfe\\u7a0b\\u9879\\u76ee\\u5c55\\u793a / Flask + \\u539f\\u751f\\u524d\\u7aef + Real-ESRGAN"),
    heroTitle: zh("\\u0052\\u0065\\u0061\\u006c\\u002d\\u0045\\u0053\\u0052\\u0047\\u0041\\u004e \\u56fe\\u50cf\\u8d85\\u5206\\u8fa8\\u7387\\u589e\\u5f3a\\u7cfb\\u7edf"),
    heroSubtitle: zh("\\u57fa\\u4e8e\\u6df1\\u5ea6\\u5b66\\u4e60\\u7684\\u56fe\\u50cf\\u8d85\\u5206\\u8fa8\\u7387\\u4e0e\\u4fee\\u590d\\u7cfb\\u7edf"),
    heroDesc: zh("\\u652f\\u6301\\u5355\\u5f20\\u56fe\\u7247\\u589e\\u5f3a\\u3001\\u6279\\u91cf\\u56fe\\u7247\\u589e\\u5f3a\\u3001\\u5c40\\u90e8\\u7ec6\\u8282\\u5bf9\\u6bd4\\u56fe\\u5c55\\u793a\\u4e0e\\u7ed3\\u679c\\u4e0b\\u8f7d\\uff0c\\u9002\\u5408\\u4f5c\\u4e3a\\u8bfe\\u7a0b\\u9879\\u76ee\\u6f14\\u793a\\u9875\\u9762\\u3002"),
    statusLabel: zh("\\u540e\\u7aef\\u72b6\\u6001"),
    tabButtonSingle: zh("\\u5355\\u5f20\\u56fe\\u7247\\u589e\\u5f3a"),
    tabButtonBatch: zh("\\u6279\\u91cf\\u56fe\\u7247\\u589e\\u5f3a"),
    tabButtonGuide: zh("\\u4f7f\\u7528\\u8bf4\\u660e"),
    singlePanelTitle: zh("\\u4e0a\\u4f20\\u4e0e\\u53c2\\u6570\\u8bbe\\u7f6e"),
    singleUploadLabel: zh("\\u4e0a\\u4f20\\u56fe\\u7247"),
    singleModelLabel: zh("\\u6a21\\u578b\\u9009\\u62e9"),
    singleOutscaleLabel: zh("\\u653e\\u5927\\u500d\\u6570"),
    singleDenoiseLabel: zh("\\u53bb\\u566a\\u5f3a\\u5ea6"),
    singleTileLabel: zh("\\u5206\\u5757\\u5927\\u5c0f"),
    singleTipTitle: zh("\\u53c2\\u6570\\u5efa\\u8bae"),
    singleTip1: zh("\\u771f\\u5b9e\\u7167\\u7247\\u5efa\\u8bae\\u4f7f\\u7528 RealESRGAN_x4plus\\u3002"),
    singleTip2: zh("\\u52a8\\u6f2b\\u6216\\u5361\\u901a\\u56fe\\u7247\\u5efa\\u8bae\\u4f7f\\u7528 RealESRGAN_x4plus_anime_6B\\u3002"),
    singleTip3: zh("\\u663e\\u5b58\\u4e0d\\u8db3\\u65f6\\u5efa\\u8bae\\u5c06\\u5206\\u5757\\u5927\\u5c0f\\u8c03\\u5c0f\\u5230 128 \\u6216 256\\u3002"),
    singleSubmitButton: zh("\\u5f00\\u59cb\\u589e\\u5f3a"),
    singleLoading: zh("\\u6b63\\u5728\\u8c03\\u7528 Real-ESRGAN \\u6a21\\u578b\\u5904\\u7406\\u56fe\\u7247\\uff0c\\u8bf7\\u7a0d\\u5019\\u2026\\u2026"),
    singleResultTitle: zh("\\u7ed3\\u679c\\u5c55\\u793a"),
    originalPreviewTitle: zh("\\u539f\\u59cb\\u56fe\\u7247\\u9884\\u89c8"),
    resultPreviewTitle: zh("\\u589e\\u5f3a\\u540e\\u56fe\\u7247\\u9884\\u89c8"),
    comparisonTitle: zh("\\u5c40\\u90e8\\u7ec6\\u8282\\u5bf9\\u6bd4\\u56fe"),
    comparisonDesc: zh("\\u5de6\\u4fa7\\u4e3a\\u539f\\u56fe\\u5c40\\u90e8\\uff0c\\u53f3\\u4fa7\\u4e3a\\u589e\\u5f3a\\u540e\\u5c40\\u90e8\\uff0c\\u4fbf\\u4e8e\\u76f4\\u89c2\\u770b\\u5230\\u7ec6\\u8282\\u53d8\\u5316\\u3002"),
    downloadButton: zh("\\u4e0b\\u8f7d\\u589e\\u5f3a\\u7ed3\\u679c"),
    comparisonDownloadButton: zh("\\u4e0b\\u8f7d\\u5c40\\u90e8\\u5bf9\\u6bd4\\u56fe"),
    batchPanelTitle: zh("\\u6279\\u91cf\\u4e0a\\u4f20\\u4e0e\\u53c2\\u6570\\u8bbe\\u7f6e"),
    batchUploadLabel: zh("\\u6279\\u91cf\\u4e0a\\u4f20\\u56fe\\u7247"),
    batchModelLabel: zh("\\u6a21\\u578b\\u9009\\u62e9"),
    batchOutscaleLabel: zh("\\u653e\\u5927\\u500d\\u6570"),
    batchDenoiseLabel: zh("\\u53bb\\u566a\\u5f3a\\u5ea6"),
    batchTileLabel: zh("\\u5206\\u5757\\u5927\\u5c0f"),
    batchSubmitButton: zh("\\u5f00\\u59cb\\u6279\\u91cf\\u589e\\u5f3a"),
    batchLoading: zh("\\u6b63\\u5728\\u6279\\u91cf\\u5904\\u7406\\u4e2d\\uff0c\\u8bf7\\u7a0d\\u5019\\u2026\\u2026"),
    batchResultTitle: zh("\\u6279\\u91cf\\u5904\\u7406\\u7ed3\\u679c"),
    batchResultDesc: zh("\\u5904\\u7406\\u5b8c\\u6210\\u540e\\uff0c\\u5c06\\u4ee5\\u5361\\u7247\\u5f62\\u5f0f\\u5c55\\u793a\\u6bcf\\u5f20\\u56fe\\u7247\\u7684\\u589e\\u5f3a\\u7ed3\\u679c\\u548c\\u5c40\\u90e8\\u5bf9\\u6bd4\\u56fe\\u3002"),
    zipDownloadButton: zh("\\u6253\\u5305\\u4e0b\\u8f7d\\u5168\\u90e8\\u7ed3\\u679c"),
    guideTitle: zh("\\u4f7f\\u7528\\u8bf4\\u660e"),
    guideIntroTitle: zh("\\u7cfb\\u7edf\\u7b80\\u4ecb"),
    guideIntroText: zh("\\u672c\\u7cfb\\u7edf\\u57fa\\u4e8e Real-ESRGAN \\u5b9e\\u73b0\\u56fe\\u50cf\\u8d85\\u5206\\u8fa8\\u7387\\u4e0e\\u4fee\\u590d\\uff0c\\u652f\\u6301\\u5355\\u5f20\\u56fe\\u7247\\u589e\\u5f3a\\u548c\\u6279\\u91cf\\u56fe\\u7247\\u589e\\u5f3a\\uff0c\\u5e76\\u81ea\\u52a8\\u751f\\u6210\\u5c40\\u90e8\\u7ec6\\u8282\\u5bf9\\u6bd4\\u56fe\\u3002"),
    guideStepsTitle: zh("\\u4f7f\\u7528\\u6b65\\u9aa4"),
    guideStep1: zh("\\u4e0a\\u4f20\\u56fe\\u7247\\u3002"),
    guideStep2: zh("\\u9009\\u62e9\\u6a21\\u578b\\u548c\\u53c2\\u6570\\u3002"),
    guideStep3: zh("\\u70b9\\u51fb\\u5f00\\u59cb\\u589e\\u5f3a\\u6216\\u5f00\\u59cb\\u6279\\u91cf\\u589e\\u5f3a\\u3002"),
    guideStep4: zh("\\u67e5\\u770b\\u539f\\u56fe\\u3001\\u589e\\u5f3a\\u56fe\\u548c\\u5c40\\u90e8\\u5bf9\\u6bd4\\u56fe\\u3002"),
    guideStep5: zh("\\u4e0b\\u8f7d\\u5904\\u7406\\u7ed3\\u679c\\u3002"),
    guideParamTitle: zh("\\u53c2\\u6570\\u8bf4\\u660e"),
    guideParam1: zh("\\u6a21\\u578b\\u9009\\u62e9\\uff1a\\u771f\\u5b9e\\u7167\\u7247\\u5efa\\u8bae\\u4f7f\\u7528 RealESRGAN_x4plus\\uff0c\\u52a8\\u6f2b\\u6216\\u5361\\u901a\\u56fe\\u7247\\u5efa\\u8bae\\u4f7f\\u7528 RealESRGAN_x4plus_anime_6B\\u3002"),
    guideParam2: zh("\\u653e\\u5927\\u500d\\u6570\\uff1a\\u4e00\\u822c\\u5efa\\u8bae\\u4f7f\\u7528 4\\u3002"),
    guideParam3: zh("\\u53bb\\u566a\\u5f3a\\u5ea6\\uff1a\\u6570\\u503c\\u8d8a\\u5927\\uff0c\\u964d\\u566a\\u8d8a\\u660e\\u663e\\uff0c\\u4f46\\u53ef\\u80fd\\u635f\\u5931\\u90e8\\u5206\\u7ec6\\u8282\\u3002"),
    guideParam4: zh("\\u5206\\u5757\\u5927\\u5c0f\\uff1a\\u663e\\u5b58\\u4e0d\\u8db3\\u65f6\\u5efa\\u8bae\\u8bbe\\u7f6e\\u4e3a 128 \\u6216 256\\uff1b\\u8bbe\\u7f6e\\u4e3a 0 \\u8868\\u793a\\u4e0d\\u5206\\u5757\\u5904\\u7406\\u3002"),
    guideNoticeTitle: zh("\\u6ce8\\u610f\\u4e8b\\u9879"),
    guideNotice1: zh("\\u652f\\u6301 jpg\\u3001jpeg\\u3001png \\u56fe\\u7247\\u3002"),
    guideNotice2: zh("\\u4e0d\\u5efa\\u8bae\\u4e0a\\u4f20\\u8fc7\\u5927\\u7684\\u56fe\\u7247\\u3002"),
    guideNotice3: zh("\\u9996\\u6b21\\u8fd0\\u884c\\u65f6\\u6a21\\u578b\\u53ef\\u80fd\\u9700\\u8981\\u4e0b\\u8f7d\\u6743\\u91cd\\uff0c\\u7b49\\u5f85\\u65f6\\u95f4\\u4f1a\\u66f4\\u957f\\u3002"),
    guideNotice4: zh("\\u6279\\u91cf\\u5904\\u7406\\u65f6\\u5efa\\u8bae\\u5148\\u7528\\u5c11\\u91cf\\u56fe\\u7247\\u6d4b\\u8bd5\\u53c2\\u6570\\u3002"),
    guideFaqTitle: zh("\\u5e38\\u89c1\\u95ee\\u9898"),
    guideFaq1: zh("\\u5982\\u679c\\u5904\\u7406\\u5931\\u8d25\\uff0c\\u53ef\\u80fd\\u662f\\u56fe\\u7247\\u8fc7\\u5927\\u3001\\u663e\\u5b58\\u4e0d\\u8db3\\u6216\\u6a21\\u578b\\u6743\\u91cd\\u8def\\u5f84\\u914d\\u7f6e\\u9519\\u8bef\\u3002"),
    guideFaq2: zh("\\u5982\\u679c\\u663e\\u5b58\\u4e0d\\u8db3\\uff0c\\u8bf7\\u8c03\\u5c0f\\u5206\\u5757\\u5927\\u5c0f\\u3002"),
    guideFaq3: zh("\\u5982\\u679c\\u7ed3\\u679c\\u56fe\\u7247\\u65e0\\u6cd5\\u663e\\u793a\\uff0c\\u8bf7\\u68c0\\u67e5\\u540e\\u7aef\\u662f\\u5426\\u5df2\\u542f\\u52a8\\u5e76\\u4fdd\\u6301\\u8fd0\\u884c\\u3002"),
    emptyBatchFiles: zh("\\u6682\\u672a\\u9009\\u62e9\\u56fe\\u7247\\u3002"),
    emptyBatchResults: zh("\\u6279\\u91cf\\u5904\\u7406\\u7ed3\\u679c\\u5c06\\u5728\\u8fd9\\u91cc\\u663e\\u793a\\u3002"),
    removeButton: zh("\\u79fb\\u9664"),
    unnamedImage: zh("\\u672a\\u547d\\u540d\\u56fe\\u7247"),
    failedMessage: zh("\\u5904\\u7406\\u5931\\u8d25\\u3002"),
    batchResultImage: zh("\\u589e\\u5f3a\\u7ed3\\u679c"),
    batchComparisonImage: zh("\\u5c40\\u90e8\\u5bf9\\u6bd4\\u56fe"),
    downloadResultImage: zh("\\u4e0b\\u8f7d\\u589e\\u5f3a\\u56fe"),
    downloadComparisonImage: zh("\\u4e0b\\u8f7d\\u5c40\\u90e8\\u5bf9\\u6bd4\\u56fe"),
    healthChecking: zh("\\u6b63\\u5728\\u68c0\\u6d4b\\u540e\\u7aef\\u670d\\u52a1\\u2026\\u2026"),
    healthOk: zh("\\u540e\\u7aef\\u8fd0\\u884c\\u6b63\\u5e38\\uff0c\\u53ef\\u5f00\\u59cb\\u4f7f\\u7528\\u3002"),
    healthUnavailablePrefix: zh("\\u540e\\u7aef\\u4e0d\\u53ef\\u7528\\uff1a"),
    healthCheckFailed: zh("\\u540e\\u7aef\\u72b6\\u6001\\u68c0\\u67e5\\u5931\\u8d25\\u3002"),
    uploadFirst: zh("\\u8bf7\\u5148\\u4e0a\\u4f20\\u56fe\\u7247\\u3002"),
    singleFailed: zh("\\u56fe\\u7247\\u589e\\u5f3a\\u5931\\u8d25\\u3002"),
    chooseBatchFirst: zh("\\u8bf7\\u5148\\u9009\\u62e9\\u9700\\u8981\\u6279\\u91cf\\u5904\\u7406\\u7684\\u56fe\\u7247\\u3002"),
    batchFailed: zh("\\u6279\\u91cf\\u589e\\u5f3a\\u5931\\u8d25\\u3002"),
    batchLoadingWithCountPrefix: zh("\\u6b63\\u5728\\u6279\\u91cf\\u5904\\u7406\\u4e2d\\uff0c\\u5171 "),
    batchLoadingWithCountSuffix: zh(" \\u5f20\\u56fe\\u7247\\uff0c\\u8bf7\\u7a0d\\u5019\\u2026\\u2026"),
};

const healthStatus = document.getElementById("healthStatus");
const tabButtons = Array.from(document.querySelectorAll(".tab-button"));
const tabPanels = Array.from(document.querySelectorAll(".tab-panel"));

const modelOptions = [
    "RealESRGAN_x4plus",
    "RealESRNet_x4plus",
    "RealESRGAN_x4plus_anime_6B",
    "RealESRGAN_x2plus",
    "realesr-animevideov3",
    "realesr-general-x4v3",
];

const imageInput = document.getElementById("imageInput");
const modelNameInput = document.getElementById("modelName");
const outscaleInput = document.getElementById("outscale");
const denoiseStrengthInput = document.getElementById("denoiseStrength");
const tileInput = document.getElementById("tile");
const submitButton = document.getElementById("submitButton");
const loadingText = document.getElementById("loadingText");
const errorMessage = document.getElementById("errorMessage");
const originalPreview = document.getElementById("originalPreview");
const resultPreview = document.getElementById("resultPreview");
const comparisonPreview = document.getElementById("comparisonPreview");
const downloadButton = document.getElementById("downloadButton");
const comparisonDownloadButton = document.getElementById("comparisonDownloadButton");

const batchImageInput = document.getElementById("batchImageInput");
const batchModelNameInput = document.getElementById("batchModelName");
const batchOutscaleInput = document.getElementById("batchOutscale");
const batchDenoiseStrengthInput = document.getElementById("batchDenoiseStrength");
const batchTileInput = document.getElementById("batchTile");
const batchSubmitButton = document.getElementById("batchSubmitButton");
const batchLoadingText = document.getElementById("batchLoadingText");
const batchErrorMessage = document.getElementById("batchErrorMessage");
const batchFileList = document.getElementById("batchFileList");
const batchResultsGrid = document.getElementById("batchResultsGrid");
const zipDownloadButton = document.getElementById("zipDownloadButton");

let batchFiles = [];

function applyStaticTexts() {
    Object.entries(textMap).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) {
            if (id === "pageTitle") {
                document.title = value;
            } else {
                element.textContent = value;
            }
        }
    });

    submitButton.textContent = textMap.singleSubmitButton;
    loadingText.textContent = textMap.singleLoading;
    batchLoadingText.textContent = textMap.batchLoading;
    originalPreview.alt = textMap.originalPreviewTitle;
    resultPreview.alt = textMap.resultPreviewTitle;
    comparisonPreview.alt = textMap.comparisonTitle;
}

function populateModelSelect(selectElement) {
    selectElement.innerHTML = "";
    modelOptions.forEach((model) => {
        const option = document.createElement("option");
        option.value = model;
        option.textContent = model;
        selectElement.appendChild(option);
    });
}

function setLinkState(linkElement, url) {
    if (url) {
        linkElement.href = url;
        linkElement.classList.remove("disabled");
        linkElement.setAttribute("aria-disabled", "false");
    } else {
        linkElement.href = "#";
        linkElement.classList.add("disabled");
        linkElement.setAttribute("aria-disabled", "true");
    }
}

function setSingleLoading(isLoading) {
    submitButton.disabled = isLoading;
    loadingText.hidden = !isLoading;
}

function setBatchLoading(isLoading) {
    batchSubmitButton.disabled = isLoading;
    batchLoadingText.hidden = !isLoading;
}

function showMessage(target, message) {
    target.textContent = message;
    target.hidden = false;
}

function clearMessage(target) {
    target.textContent = "";
    target.hidden = true;
}

function switchTab(tabName) {
    tabButtons.forEach((button) => {
        button.classList.toggle("active", button.dataset.tab === tabName);
    });
    tabPanels.forEach((panel) => {
        panel.classList.toggle("active", panel.id === `tab-${tabName}`);
    });
}

function formatFileSize(size) {
    if (size < 1024) {
        return `${size} B`;
    }
    if (size < 1024 * 1024) {
        return `${(size / 1024).toFixed(1)} KB`;
    }
    return `${(size / (1024 * 1024)).toFixed(2)} MB`;
}

function resetSingleResult() {
    resultPreview.removeAttribute("src");
    comparisonPreview.removeAttribute("src");
    setLinkState(downloadButton, "");
    setLinkState(comparisonDownloadButton, "");
}

function renderBatchFileList() {
    if (batchFiles.length === 0) {
        batchFileList.innerHTML = `<p class="empty-text">${textMap.emptyBatchFiles}</p>`;
        return;
    }

    batchFileList.innerHTML = "";
    batchFiles.forEach((file, index) => {
        const item = document.createElement("div");
        item.className = "file-item";
        item.innerHTML = `
            <span class="file-name" title="${file.name}">${file.name}</span>
            <span class="file-size">${formatFileSize(file.size)}</span>
            <button type="button" class="file-remove-button" data-index="${index}">${textMap.removeButton}</button>
        `;
        batchFileList.appendChild(item);
    });

    batchFileList.querySelectorAll(".file-remove-button").forEach((button) => {
        button.addEventListener("click", () => {
            const index = Number(button.dataset.index);
            batchFiles.splice(index, 1);
            renderBatchFileList();
        });
    });
}

function renderBatchResults(results) {
    if (!results.length) {
        batchResultsGrid.innerHTML = `<p class="empty-text">${textMap.emptyBatchResults}</p>`;
        return;
    }

    batchResultsGrid.innerHTML = "";
    results.forEach((item) => {
        const card = document.createElement("article");
        card.className = `batch-result-card${item.success ? "" : " failed"}`;

        if (!item.success) {
            card.innerHTML = `
                <h3>${item.original_name || textMap.unnamedImage}</h3>
                <p class="batch-meta">${item.message || textMap.failedMessage}</p>
            `;
            batchResultsGrid.appendChild(card);
            return;
        }

        card.innerHTML = `
            <h3>${item.original_name}</h3>
            <p class="batch-meta">${item.message}</p>
            <div class="batch-result-preview">
                <div>
                    <h4>${textMap.batchResultImage}</h4>
                    <div class="image-frame">
                        <img src="${item.result_url}" alt="${textMap.batchResultImage}">
                    </div>
                </div>
                <div>
                    <h4>${textMap.batchComparisonImage}</h4>
                    <div class="image-frame">
                        <img src="${item.comparison_url}" alt="${textMap.batchComparisonImage}">
                    </div>
                </div>
            </div>
            <div class="batch-result-actions">
                <a class="ghost-button" href="${item.download_url}" download>${textMap.downloadResultImage}</a>
                <a class="ghost-button" href="${item.comparison_download_url}" download>${textMap.downloadComparisonImage}</a>
            </div>
        `;
        batchResultsGrid.appendChild(card);
    });
}

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        if (!response.ok || !data.success) {
            throw new Error(data.message || textMap.healthCheckFailed);
        }

        if (Array.isArray(data.models) && data.models.length) {
            modelOptions.length = 0;
            data.models.forEach((model) => modelOptions.push(model));
            populateModelSelect(modelNameInput);
            populateModelSelect(batchModelNameInput);
        }

        if (data.defaults) {
            outscaleInput.value = data.defaults.outscale;
            denoiseStrengthInput.value = data.defaults.denoise_strength;
            tileInput.value = data.defaults.tile;
            batchOutscaleInput.value = data.defaults.outscale;
            batchDenoiseStrengthInput.value = data.defaults.denoise_strength;
            batchTileInput.value = data.defaults.tile;
            modelNameInput.value = data.defaults.model_name;
            batchModelNameInput.value = data.defaults.model_name;
        }

        healthStatus.textContent = textMap.healthOk;
    } catch (error) {
        healthStatus.textContent = `${textMap.healthUnavailablePrefix}${error.message}`;
    }
}

imageInput.addEventListener("change", () => {
    clearMessage(errorMessage);
    resetSingleResult();

    const [file] = imageInput.files;
    if (!file) {
        originalPreview.removeAttribute("src");
        return;
    }

    originalPreview.src = URL.createObjectURL(file);
});

submitButton.addEventListener("click", async () => {
    clearMessage(errorMessage);
    resetSingleResult();

    const [file] = imageInput.files;
    if (!file) {
        showMessage(errorMessage, textMap.uploadFirst);
        return;
    }

    const formData = new FormData();
    formData.append("image", file);
    formData.append("model_name", modelNameInput.value);
    formData.append("outscale", outscaleInput.value);
    formData.append("denoise_strength", denoiseStrengthInput.value);
    formData.append("tile", tileInput.value);

    setSingleLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/api/upscale`, {
            method: "POST",
            body: formData,
        });
        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.message || textMap.singleFailed);
        }

        originalPreview.src = data.original_url;
        resultPreview.src = data.result_url;
        comparisonPreview.src = data.comparison_url;
        setLinkState(downloadButton, data.download_url);
        setLinkState(comparisonDownloadButton, data.comparison_download_url);
    } catch (error) {
        showMessage(errorMessage, error.message);
    } finally {
        setSingleLoading(false);
    }
});

batchImageInput.addEventListener("change", () => {
    clearMessage(batchErrorMessage);
    batchFiles = Array.from(batchImageInput.files);
    renderBatchFileList();
});

batchSubmitButton.addEventListener("click", async () => {
    clearMessage(batchErrorMessage);
    renderBatchResults([]);
    setLinkState(zipDownloadButton, "");

    if (!batchFiles.length) {
        showMessage(batchErrorMessage, textMap.chooseBatchFirst);
        return;
    }

    const formData = new FormData();
    batchFiles.forEach((file) => {
        formData.append("images", file);
    });
    formData.append("model_name", batchModelNameInput.value);
    formData.append("outscale", batchOutscaleInput.value);
    formData.append("denoise_strength", batchDenoiseStrengthInput.value);
    formData.append("tile", batchTileInput.value);

    setBatchLoading(true);
    batchLoadingText.textContent = `${textMap.batchLoadingWithCountPrefix}${batchFiles.length}${textMap.batchLoadingWithCountSuffix}`;

    try {
        const response = await fetch(`${API_BASE_URL}/api/batch-upscale`, {
            method: "POST",
            body: formData,
        });
        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.message || textMap.batchFailed);
        }

        renderBatchResults(data.results || []);
        setLinkState(zipDownloadButton, data.zip_download_url || "");
    } catch (error) {
        showMessage(batchErrorMessage, error.message);
    } finally {
        setBatchLoading(false);
        batchLoadingText.textContent = textMap.batchLoading;
    }
});

tabButtons.forEach((button) => {
    button.addEventListener("click", () => switchTab(button.dataset.tab));
});

applyStaticTexts();
healthStatus.textContent = textMap.healthChecking;
populateModelSelect(modelNameInput);
populateModelSelect(batchModelNameInput);
renderBatchFileList();
renderBatchResults([]);
checkHealth();
