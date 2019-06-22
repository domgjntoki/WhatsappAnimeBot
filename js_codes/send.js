window.sendMsg = function(id, msg) {
    if (window.Store === undefined) {
        try{
            webpackJsonp([], {"bcihgfbdeb": (x, y, z) => window.Store = z('"bcihgfbdeb"')}, "bcihgfbdeb");
            webpackJsonp([], {"iaeeehaci": (x, y, z) => window.Store.Wap = z('"iaeeehaci"')}, "iaeeehaci");
        } catch (e) {}
    }
    Store.Chat.models[id].sendMessage(msg);
}

window.sendMsg2 = function (id, text) {
    if (window.Store === undefined) {
        try{
            webpackJsonp([], {"bcihgfbdeb": (x, y, z) => window.Store = z('"bcihgfbdeb"')}, "bcihgfbdeb");
            webpackJsonp([], {"iaeeehaci": (x, y, z) => window.Store.Wap = z('"iaeeehaci"')}, "iaeeehaci");
        } catch (e) {}
    }

    var Chats = Store.Chat.models;
    var contact = id;
    var message = text;
    for (chat in Chats) {
        if (isNaN(chat)) {
            continue;
        };
        var temp = {};
        temp.contact = Chats[chat].__x__formattedTitle;
        temp.id = Chats[chat].__x_id._serialized;
        if(temp.id.search(contact)!= -1) {
            Chats[chat].sendMessage(message);
            return true;
        }
    }
}