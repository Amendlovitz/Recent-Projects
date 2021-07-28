const moment = require('moment');

function formatMsg(info){
    return {
        info,
        time: moment().format('h:mm a')
    }
}

module.exports = formatMsg;