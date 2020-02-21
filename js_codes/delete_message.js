
// The chat_id is in chat.__x_id._serialized;
window.deleteMessage = function(chat_id, msg) {
    if (window.Store === undefined) {
        try{
            webpackJsonp([], {"bcihgfbdeb": (x, y, z) => window.Store = z('"bcihgfbdeb"')}, "bcihgfbdeb");
            webpackJsonp([], {"iaeeehaci": (x, y, z) => window.Store.Wap = z('"iaeeehaci"')}, "iaeeehaci");
        } catch (e) {}
    }
    Chats = Store.Chat.models
    for(chat in Chats) {
        if (isNaN(chat)) {
            continue;
        };
        temp_id = Chats[chat].__x_id._serialized;
        if(temp_id.search(chat_id) != -1){
            messages = Chats[chat].msgs.models
            for(message in messages) {
                temp_msg = messages[message]
                if(temp_msg.__x_text == msg && temp_msg.canRevoke()) {
                    temp_msg.sendRevoke(temp_msg)
                    //return true;
                }
            }
        }
    }
}