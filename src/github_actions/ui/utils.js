function format_timestamp(datetime, format) {
    if (typeof format == 'undefined') {
        format = "[ ddd ] MMM dd, yyyy hh:mm:ss"
    }
    return new Date(Date.parse(datetime)).toLocaleString(Qt.locale('en_US'), format)
}

function a_insert(arr, val) {
    arr.push(val)
}

function a_delete(arr, val) {
    const idx = arr.indexOf(val)
    if (idx > -1) {
        arr.splice(idx, 1)
    }
}

function a_insert2(arr, val, insert=true) {
    if (insert) {
        a_insert(arr, val)
    } else {
        a_delete(arr, val)
    }
    // console.log(arr)
}
