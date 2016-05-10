/******************************************************************************
*
*    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
*    All Rights Reserved
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU Affero General Public License as
*    published by the Free Software Foundation, either version 3 of the
*    License, or (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU Affero General Public License for more details.
*
*    You should have received a copy of the GNU Affero General Public License
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
******************************************************************************/
openerp_announcement = function(instance) {

};



function LHready() {
    if(document.readyState == "complete") {
        (function(){
            var lh=document.createElement("script");
            lh.type="text/javascript";
            lh.async=true;
            lh.src="//server.livehelp.it/widgetjs/72663/802.js?x=" + 1*new Date();
            var node=document.getElementsByTagName("script")[0];
            node.parentNode.insertBefore(lh,node);
         })();
     } else {
        setTimeout('LHready()',150);
     }
} LHready();
