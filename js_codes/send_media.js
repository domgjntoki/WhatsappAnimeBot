window.base64ImageToFile = function(base64, filename) {
	var arr   = b64Data.split(',');
    var mime  = arr[0].match(/:(.*?);/)[1];
    var bstr  = atob(arr[1]);
    var n     = bstr.length;
    var u8arr = new Uint8Array(n);

    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }

    return new File([u8arr], filename, {type: mime});
} 
window.send_media = function(jid, base64, caption, msg_id) {
	var done = null;
	var filename = "temp";
	var idUser = new window.Store.UserConstructor(jid, { intentionallyUsePrivateConstructor: true });
	return Store.Chat.find(idUser).then((chat) => {
		var mediaBlob = window.base64ImageToFile(base64, filename);
		var mc = new Store.MediaCollection();
		var target = _.filter(window.Store.Msg.models, (msg) => {
			return msg.id.id === msg_id;
		})[0];
		mc.processFiles([mediaBlob], chat, 1).then(() => {
			var media = mc.models[0];
			media.sendToChat(chat, { caption: caption, quotedMsg: target });
			if (done !== undefined) done(true);
		});
	});
}
