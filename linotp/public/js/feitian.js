/*!
 *   LinOTP - the open source solution for two factor authentication
 *   Copyright (C) 2010 - 2019 KeyIdentity GmbH
 *
 *   This file is part of LinOTP server.
 *
 *   This program is free software: you can redistribute it and/or
 *   modify it under the terms of the GNU Affero General Public
 *   License, version 3, as published by the Free Software Foundation.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU Affero General Public License for more details.
 *
 *   You should have received a copy of the
 *              GNU Affero General Public License
 *   along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *
 *    E-mail: linotp@keyidentity.com
 *    Contact: www.linotp.org
 *    Support: www.keyidentity.com
 *
 */
function create_feitian_dialog() {
    var $dialog_load_tokens_feitian = $('#dialog_import_feitian').dialog({
        autoOpen: false,
        title: 'Feitian XML Token file',
        width: 600,
        modal: true,
        buttons: {
            'load token file': {
                click: function () {
                    load_tokenfile('feitian');
                    $(this).dialog('close');
                },
                id: "button_feitian_load",
                text: "load token file"
            },
            Cancel: {
                click: function () {
                    $(this).dialog('close');
                },
                id: "button_feitian_cancel",
                text: "Cancel"
            }
        },
        open: function () {
            _fill_realms($('#feitian_realm'), 1);

            $(this).dialog_icons();
            translate_import_feitian();
        }
    });
    return $dialog_load_tokens_feitian;
}