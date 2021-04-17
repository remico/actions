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
import QtQuick 2.15
import QtQuick.Layouts 1.15

FocusScope {
    id: _buttons

    default property alias buttons: _c.children

    focus: true

    ColumnLayout {
        id: _c
        onChildrenChanged: children[0] ? children[0].focus = true : null
    }
}
