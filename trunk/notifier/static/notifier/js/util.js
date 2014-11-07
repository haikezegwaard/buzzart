function drawMyCircels(id, difference) {
    var canvas = document.getElementById(id);
    var context = canvas.getContext('2d');
    var height = 26 * (Math.sqrt(3) / 2);
    var X = 75;
    var Y = 35;

    var Xmin = 75;
    var Ymin = 57;

    var centerX = canvas.width / 2;
    var centerY = canvas.height / 2;
    var radius = 55;

    context.beginPath();
    context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
    if (difference > 0) {
        context.fillStyle = '#00acb7';
    } else if (difference == 0) {
        context.fillStyle = '#af248e';
    } else {
        context.fillStyle = '#ed266b';
    }
    context.fill();
    context.font = '15pt Tahoma';
    context.fillStyle = 'white';
    context.textAlign = 'center'
    if (difference > 0) {
        context.fillText('+'+difference, centerX, 110);
    } else if (difference == 0) {
        context.fillText(difference, centerX, 110);
    } else {
        context.fillText('-'+difference, centerX, 110);
    }

    if (difference > 0) {
        context.beginPath();
        context.moveTo(X, Y);
        context.lineTo(X + 13, Y + height);
        context.lineTo(X - 13, Y + height);
        context.lineTo(X, Y);
        context.fillStyle = 'white';
        context.fill();
    } else if (difference == 0) {
        context.beginPath();
        context.moveTo(63, 54);
        context.lineTo(89, 54);
        context.lineWidth = 6;
        context.strokeStyle = '#ffffff';
        context.lineCap = 'square';
        context.stroke();
    } else {
        context.beginPath();
        context.moveTo(Xmin, Ymin);
        context.lineTo(Xmin + 13, Ymin - height);
        context.lineTo(Xmin - 13, Ymin - height);
        context.lineTo(Xmin, Ymin);
        context.fillStyle = 'white';
        context.fill();
    }

    context.beginPath();
    context.moveTo(30, 77);
    context.lineTo(119, 77);
    context.lineWidth = 2;
    context.strokeStyle = 'rgba(255,255,255,0.6)';
    context.lineCap = 'square';
    context.stroke();
    image = convertCanvasToImage(canvas);
    canvas.parentNode.replaceChild(image, canvas);
}

// Converts canvas to an image

function convertCanvasToImage(canvas) {
    var image = new Image();
    image.src = canvas.toDataURL("image/png");
    return image;
}

function getImgData(chartContainer) {
    var chartArea = chartContainer.getElementsByTagName('svg')[0].parentNode;
    var svg = chartArea.innerHTML;
    var doc = chartContainer.ownerDocument;
    var canvas = doc.createElement('canvas');
    canvas.setAttribute('width', chartArea.offsetWidth);
    canvas.setAttribute('height', chartArea.offsetHeight);

    canvas.setAttribute(
        'style',
        'position: absolute; ' +
        'top: ' + (-chartArea.offsetHeight * 2) + 'px;' +
        'left: ' + (-chartArea.offsetWidth * 2) + 'px;');
    doc.body.appendChild(canvas);
    canvg(canvas, svg);
    var imgData = canvas.toDataURL("image/png");
    canvas.parentNode.removeChild(canvas);
    return imgData;
}

function saveAsImg(chartContainer) {
    var imgData = getImgData(chartContainer);

    // Replacing the mime-type will force the browser to trigger a download
    // rather than displaying the image in the browser window.
    window.location = imgData.replace("image/png", "image/octet-stream");
}

function toImg(chartContainer, imgContainer) {
    var doc = chartContainer.ownerDocument;
    var img = doc.createElement('img');
    img.src = getImgData(chartContainer);

    while (imgContainer.firstChild) {
        imgContainer.removeChild(imgContainer.firstChild);
    }
    imgContainer.appendChild(img);
}