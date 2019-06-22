window.isChatMessage = function (message) {
   // if (message.__x_isSentByMe ) {
  //      return false;
  //  }
    if (message.__x_isNotification) {
        return false;
    }
    if (!message.__x_isUserCreatedType) {
        return false;
    }
    return true;
}

window.readMessages = function(chat_index) {
    if (window.Store === undefined) {
        try{
            webpackJsonp([], {"bcihgfbdeb": (x, y, z) => window.Store = z('"bcihgfbdeb"')}, "bcihgfbdeb");
            webpackJsonp([], {"iaeeehaci": (x, y, z) => window.Store.Wap = z('"iaeeehaci"')}, "iaeeehaci");
        } catch (e) {}
    }

    var chat = Store.Chat.models[chat_index];

    var temp = {};
    temp.contact = chat.__x_formattedTitle;
    temp.messages = [];
    var messages = chat.msgs.models;

    for (var i = messages.length - 1; i >= 0; i--) {
        if (!messages[i].__x_isNewMsg) {
            break;
        } else {
            if (!isChatMessage(messages[i])) {
                continue;
            }
            messages[i].__x_isNewMsg = false;
            temp.messages.push({
                id: messages[i].__x_id.id,
                message: messages[i].__x_body,
                timestamp: messages[i].__x_t,
                type : messages[i].__x_type
            });
        }
    }
    return JSON.stringify(temp);
}

window.getUnreadChats = function () {
    if (window.Store === undefined) {
        try{
            webpackJsonp([], {"bcihgfbdeb": (x, y, z) => window.Store = z('"bcihgfbdeb"')}, "bcihgfbdeb");
            webpackJsonp([], {"iaeeehaci": (x, y, z) => window.Store.Wap = z('"iaeeehaci"')}, "iaeeehaci");
        } catch (e) {}
    }

    var Chats = Store.Chat.models;
    var Output = [];

    for (chat in Chats) {
        if (isNaN(chat)) {
            continue;
        };
        var temp = {};
        temp.contact = Chats[chat].__x_formattedTitle;
        if (Chats[chat].isGroup) {
            temp.participants = []
            participants = Chats[chat].groupMetadata.participants.models
            for (var i = 0; i < participants.length; i++) {
                temp.participants.push({
                    id: participants[i].id.user,
                    contact: participants[i].contact.notifyName
                })
            }
        } else {
            temp.participants = []
        }

        temp.id = Chats[chat].__x_id._serialized;
        temp.messages = [];
        var messages = Chats[chat].msgs.models;
        for (var i = messages.length - 1; i >= 0; i--) {
            if (!messages[i].__x_isNewMsg) {
                break;
            } else {
                if (!isChatMessage(messages[i])) {
                    continue
                }
                messages[i].__x_isNewMsg = false;
                temp.messages.push({
                    id: messages[i].__x_sender.user,
                    contact: messages[i].senderObj.notifyName,
                    msg_id: messages[i].__x_id.id,
                    message: messages[i].__x_text,
                    type: messages[i].__x_type,
                    timestamp: messages[i].__x_t,
                    type: messages[i].__x_type,
                    e: messages[i]
                });
            }
        }
        if(temp.messages.length > 0) {
            Output.push(temp);
        }
    }
    return JSON.stringify(Output);
}