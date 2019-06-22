setTimeout(function() {
function getAllModules() {
    return new Promise((resolve) => {
        const id = _.uniqueId("fakeModule_");
        window["webpackJsonp"](
            [],
            {
                [id]: function(module, exports, __webpack_require__) {
                    resolve(__webpack_require__.c);
                }
            },
            [id]
        );
    });
}

var modules = getAllModules()._value;

for (var key in modules) {
	if (modules[key].exports) {
		if (modules[key].exports.createFromData) {
			createFromData_id = modules[key].id.replace(/"/g, '"');
		}
		if (modules[key].exports.prepRawMedia) {
			prepareRawMedia_id = modules[key].id.replace(/"/g, '"');
		}
		if (modules[key].exports.default) {
			if (modules[key].exports.default.Wap) {
				store_id = modules[key].id.replace(/"/g, '"');
			}
		}
	}
}

}, 2000);



function _requireById(id) {
	return webpackJsonp([], null, [id]);
}

var createFromData_id = 0;
var prepareRawMedia_id = 0;
var store_id = 0;

function fixBinary (bin) {
	var length = bin.length;
	var buf = new ArrayBuffer(length);
	var arr = new Uint8Array(buf);
	for (var i = 0; i < length; i++) {
	  arr[i] = bin.charCodeAt(i);
	}
	return buf;
}

var send_media;
window.send_media = function(jid, link, caption, msg_id) {
	var file = "";
	var createFromDataClass = _requireById(createFromData_id)["default"];
	var prepareRawMediaClass = _requireById(prepareRawMedia_id).prepRawMedia;
	window.Store.Chat.find(jid).then((chat) => {
		chat.markComposing();
		var img_b64 = link;
		var base64 = img_b64.split(',')[1];
		var type = img_b64.split(',')[0];
		type = type.split(';')[0];
		type = type.split(':')[1];
		var binary = fixBinary(atob(base64));
		var blob = new Blob([binary], {type: type});
		var random_name = Math.random().toString(36).substr(2, 5);
		file = new File([blob], random_name, {
			type: type,
			lastModified: Date.now()
		});

		var temp = createFromDataClass.createFromData(file, file.type);
		var rawMedia = prepareRawMediaClass(temp, {});
		var target = _.filter(window.Store.Msg.models, (msg) => {
			return msg.id.id === msg_id;
		})[0];
		var textPortion = {
			caption: caption,
			mentionedJidList: [],
			quotedMsg: target
		};
		rawMedia.sendToChat(chat, textPortion);


	});
}