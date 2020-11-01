/*
 * This file is part of "github actions gui" project
 *
 * Author: Roman Gladyshev <remicollab@gmail.com>
 * License: MIT License
 *
 * SPDX-License-Identifier: MIT
 * License text is available in the LICENSE file and online:
 * http://www.opensource.org/licenses/MIT
 *
 * Copyright (c) 2020 remico
 */

 function format_timestamp(datetime, format) {
    if (typeof format == 'undefined') {
        format = "[ ddd ] MMM dd, yyyy hh:mm:ss"
    }
    return new Date(Date.parse(datetime)).toLocaleString(Qt.locale('en_US'), format)
}

function time_delta_formatted(datetime) {
    var now = new Date();
    var old = new Date(Date.parse(datetime));
    var diffMs = (now - old); // milliseconds between now & the datetime
    var diffDays = Math.floor(diffMs / 86400000); // days
    var diffHrs = Math.floor((diffMs % 86400000) / 3600000); // hours
    var diffMins = Math.floor(((diffMs % 86400000) % 3600000) / 60000); // minutes
    var diffSec = Math.round(diffMs / 1000); // seconds

    if (diffDays) return diffDays + " day(s) ago"
    else if (diffHrs) return diffHrs + " hour(s) ago"
    else if (diffMins) return diffMins + " min ago"
    else return diffSec + " sec ago"
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
