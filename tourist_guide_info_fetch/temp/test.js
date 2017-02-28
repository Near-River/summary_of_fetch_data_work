function MM_reloadPage(init) {
    if (init == true) with (navigator) {
        if ((appName == "Netscape") && (parseInt(appVersion) == 4)) {
            document.MM_pgW = innerWidth;
            document.MM_pgH = innerHeight;
            onresize = MM_reloadPage;
        }
    }
    else if (innerWidth != document.MM_pgW || innerHeight != document.MM_pgH) location.reload();
}

MM_reloadPage(true);
nereidFadeObjects = new Object();
nereidFadeTimers = new Object();

function nereidFade(object, destOp, rate, delta) {
    if (!document.all)
        return
    if (object != "[object]") {
        setTimeout("nereidFade(" + object + "," + destOp + "," + rate + "," + delta + ")", 0);
        return;
    }
    clearTimeout(nereidFadeTimers[object.sourceIndex]);
    diff = destOp - object.filters.alpha.opacity;
    direction = 1;
    if (object.filters.alpha.opacity > destOp) {
        direction = -1;
    }
    delta = Math.min(direction * diff, delta);
    object.filters.alpha.opacity += direction * delta;
    if (object.filters.alpha.opacity != destOp) {
        nereidFadeObjects[object.sourceIndex] = object;
        nereidFadeTimers[object.sourceIndex] = setTimeout("nereidFade(nereidFadeObjects[" + object.sourceIndex + "]," + destOp + "," + rate + "," + delta + ")", rate);
    }
}

function login_check() {
    if (form_loginx.text_username.value == "") {
        alert("ÊäÈë´íÎó£¬ÇëÊäÈëÓÃ»§Ãû!");
        return false;
    }
    if (form_loginx.text_password.value == "") {
        alert("ÊäÈë´íÎó£¬ÇëÊäÈëÓÃ»§ÃÜÂë!");
        return false;
    }
}

function alert_submit_01() {
    if (confirm("ÇëÈ·ÈÏ£¬ËùÑ¡ÔñÖÐµ¼ÓÎÔ±ÄêÉóÍê³É?")) {
        return true;
    }
    else {
        return false;
    }
}

function alert_submit_02() {
    if (confirm("ÇëÈ·ÈÏÐÅÏ¢£¬²¢Ìí¼Ó¸ÃÓÃ»§?")) {
        return true;
    }
    else {
        return false;
    }
}

function alert_submit_password_modi() {
    if (confirm("ÇëÈ·ÈÏÐÅÏ¢£¬²¢ÐÞ¸Ä¸ÃÓÃ»§ÐÅÏ¢?")) {
        return true;
    }
    else {
        return false;
    }
}

function selectlogin_check1() {
    if ((form_selectlogin1.text_dyzh.value == "") && (form_selectlogin1.text_dykh.value == "") && (form_selectlogin1.text_dysfzh.value == "")) {
        alert("ÊäÈë´íÎó£¡µ¼ÓÎÖ¤ºÅ¡¢µ¼ÓÎ¿¨ºÅ¡¢Éí·ÝÖ¤ºÅ±ØÐëÌîÐ´Ò»Ïî£¡");
        return false;
    }
}

function selectlogin_check2() {
    if ((form_selectlogin2.text_jczh.value == "") && (form_selectlogin2.text_jckh.value == "") && (form_selectlogin2.text_jcsfzh.value == "")) {
        alert("ÊäÈë´íÎó£¡¼ì²éÖ¤ºÅ¡¢¼ì²é¿¨ºÅ¡¢Éí·ÝÖ¤ºÅ±ØÐëÌîÐ´Ò»Ïî£¡");
        return false;
    }
}

function radio_select(var1) {
    if (var1 == 0) {
        location.assign("./index_99_04_yearcheckup.asp");
    }
    else {
        location.assign("./index_99_04_yearcheckup_" + var1 + ".asp");
    }
}

function search_sub_02(var3) {
    var1 = search_field.options[search_field.selectedIndex].value;
    var2 = search_var.value;
    if (var2 == "") {
        alert("²éÑ¯´íÎó£¬ÇëÊäÈë²éÑ¯Öµ£¡");
        return;
    }
    location.assign("./" + var3 + "?search_field=" + var1 + "&search_var=" + var2);
}

function text_click() {
    if (search_var.value.indexOf(".") > 0) {
        search_var.value = "";
    }
}

function image_num_sub(var1) {
    var num_str = String(var1);
    var num_img = "";
    for (i = 0; i < num_str.length; i++) {
        num_img = num_img + "<img src='../images/n_" + num_str.charAt(i) + ".jpg'>";
    }
    document.write(num_img);
}

function select_all(var1) {
    for (var i = 0; i < form1.elements.length; i++) {
        if (form1.elements[i].type == "checkbox") {
            form1.elements[i].checked = var1;
        }
    }
}

function search2(var1, var2, var3) {
    location.assign("./index_01_01_detail_grade.asp?areacode=" + var3 + "&areaname=" + var2 + "&grade_code=" + var1);
}

function search3(var1, var2, var3) {
    location.assign("./index_02_02_detail_city.asp?areaname=" + var2 + "&areacode=" + var3 + "&radio_area=" + var1);
}

function search4(var1, var2, var3) {
    location.assign("./index_01_02_detail_city.asp?areacode=" + var3 + "&areaname=" + var2 + "&lang_code=" + var1);
}

function search5(var1, var2, var3) {
    location.assign("./index_01_05_detail_city.asp?areacode=" + var3 + "&areaname=" + var2 + "&reward_code=" + var1);
}

function search6(var1, var2, var3) {
    location.assign("./index_02_02_detail_city.asp?areacode=" + var3 + "&areaname=" + var2 + "&fz=" + var1);
}

function search7(var1, var2, var3) {
    location.assign("./index_03_02_detail_city.asp?areacode=" + var3 + "&areaname=" + var2 + "&ispx=" + var1);
}

function help_show(obj) {
    if (event.clientX >= 650) {
        help_div.style.posLeft = event.clientX + document.body.scrollLeft - 410;
        help_div.style.posTop = event.clientY + document.body.scrollTop + 10;
    }
    else {
        help_div.style.posLeft = event.clientX + document.body.scrollLeft - 10;
        help_div.style.posTop = event.clientY + document.body.scrollTop + 10;
    }
    help_div.style.visibility = '';
    help_div.style.textAlign = 'left';
    help_div.innerHTML = "<font style=vertical-align:sub;>&nbsp;&nbsp;" + obj + "</font>";
}
function help_hide() {
    help_div.style.visibility = 'hidden'
}

function clipboard_copy() {
    form1.tt1.focus();
    form1.tt1.select();
    document.execCommand('copy');
    alert('Í¼Æ¬µØÖ·ÒÑ¸´ÖÆÍê³É£¡');
}

function load_admin() {
    location.assign("./index_admin_01.asp");
}

function login_check_01() {
    if (form_loginx.username.value == "") {
        alert("ÇëÊäÈëÓÃ»§ºÍÃÜÂë£¡");
        form_loginx.username.focus();
        return false;
    }
    if (form_loginx.password.value == "") {
        alert("ÇëÊäÈëÓÃ»§ºÍÃÜÂë£¡");
        form_loginx.password.focus();
        return false;
    }
}

function alert_info_ck_delete(var1) {
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÌõ¼ÇÂ¼Âð£¿")) {
        location.assign("./info_ck_edit.asp?action=delete&info_id=" + var1);
    }
}

function alert_news_delete(var1) {
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÌõ¼ÇÂ¼Âð£¿")) {
        location.assign("./news_edit.asp?action=delete&news_id=" + var1);
    }
}

function alert_tech_delete(var1) {
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÌõ¼ÇÂ¼Âð£¿")) {
        location.assign("./technology_gc_edit.asp?action=delete&tech_id=" + var1);
    }
}

function alert_download_delete(var1) {
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÌõ¼ÇÂ¼Âð£¿")) {
        location.assign("./tech_download_edit.asp?action=delete&down_id=" + var1);
    }
}

function alert_technology_gc_delete(var1) {
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÌõ¼ÇÂ¼Âð£¿")) {
        location.assign("./technology_gc_edit.asp?action=delete&tech_id=" + var1);
    }
}

function alert_notify_delete(var1) {
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÌõ¼ÇÂ¼Âð£¿")) {
        location.assign("./notify_tz_edit.asp?action=delete&notify_id=" + var1);
    }
}

function alert_theme_delete(var1) {
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÌõ¼ÇÂ¼Âð£¿")) {
        location.assign("./theme_zt_edit.asp?action=delete&theme_id=" + var1);
    }
}

function alert_twhh_delete(var1) {
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÌõ¼ÇÂ¼Âð£¿")) {
        location.assign("./twhh_edit.asp?action=delete&twhh_id=" + var1);
    }
}

function alert_jzcm_delete(var1) {
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÌõ¼ÇÂ¼Âð£¿")) {
        location.assign("./jzcm_edit.asp?action=delete&jzcm_id=" + var1);
    }
}

function alert_ymtx_delete(var1) {
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÌõ¼ÇÂ¼Âð£¿")) {
        location.assign("./ymtx_edit.asp?action=delete&ymtx_id=" + var1);
    }
}

function alert_img_delete_1(var1) {
    if (confirm("É¾³ýÍ¼Æ¬£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÍ¼Æ¬Âð£¿")) {
        location.assign("./upload_img_edit.asp?action=delete&img_name=" + var1);
    }
}

function alert_file_delete_1(var1)    //Í¨ÖªÍ¨¸æ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ý¸½¼þ£¬ÇëÈ·ÈÏÉ¾³ý¸Ã¸½¼þÂð£¿")) {
        location.assign("./notify_tz_edit.asp?action=file_delete&notify_id=" + var1);
    }
}

function alert_info_delete_2(var1, var2)    //ÐÅÏ¢²Î¿¼-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ýÍ¼Æ¬£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÍ¼Æ¬Âð£¿")) {
        location.assign("./info_ck_edit.asp?action=file_delete&info_id=" + var1 + "&img_id=" + var2);
    }
}

function alert_news_delete_1(var1, var2)    //¾¯½ç·çÔÆ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ýÍ¼Æ¬£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÍ¼Æ¬Âð£¿")) {
        location.assign("./news_edit.asp?action=file_delete&news_id=" + var1 + "&img_id=" + var2);
    }
}

function alert_operation_delete_1(var1, var2)    //¾¯½ç·çÔÆ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ýÍ¼Æ¬£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÍ¼Æ¬Âð£¿")) {
        location.assign("./operation_dt_edit.asp?action=file_delete&operation_id=" + var1 + "&img_id=" + var2);
    }
}

function alert_operation_delete(var1) {
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÌõ¼ÇÂ¼Âð£¿")) {
        location.assign("./operation_dt_edit.asp?action=delete&operation_id=" + var1);
    }
}

function alert_experience_delete_1(var1, var2)    //¾­Ñé½»Á÷-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ýÍ¼Æ¬£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÍ¼Æ¬Âð£¿")) {
        location.assign("./experience_jl_edit.asp?action=file_delete&experience_id=" + var1 + "&img_id=" + var2);
    }
}

function alert_experience_delete_2(var1, var2)    //¾­Ñé½»Á÷-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ýÍ¼Æ¬£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÍ¼Æ¬Âð£¿")) {
        location.assign("./experience_jl_edit.asp?action=delete&experience_id=" + var1);
    }
}

function alert_theme_delete_1(var1, var2)    //×¨ÌâÉèÖÃ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ýÍ¼Æ¬£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÍ¼Æ¬Âð£¿")) {
        location.assign("./theme_zt_edit.asp?action=file_delete&theme_id=" + var1 + "&img_id=" + var2);
    }
}

function alert_twhh_delete_1(var1, var2)    //ÌìÍø»Ö»Ö-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸Ã¼ÇÂ¼Âð£¿")) {
        location.assign("./twhh_edit.asp?action=file_delete&twhh_id=" + var1 + "&img_id=" + var2);
    }
}

function alert_jzcm_delete_1(var1, var2)    //ÌìÍø»Ö»Ö-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸Ã¼ÇÂ¼Âð£¿")) {
        location.assign("./jzcm_edit.asp?action=file_delete&jzcm_id=" + var1 + "&img_id=" + var2);
    }
}

function alert_ymtx_delete_1(var1, var2)    //ÓþÂúÌìÏÂ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸Ã¼ÇÂ¼Âð£¿")) {
        location.assign("./ymtx_edit.asp?action=file_delete&ymtx_id=" + var1 + "&img_id=" + var2);
    }
}

function alert_jsl_delete_1(var1, var2)    //¾¯Ê¾À¸-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸Ã¼ÇÂ¼Âð£¿")) {
        location.assign("./jsl_edit.asp?action=delete&jsl_id=" + var1 + "&img_id=" + var2);
    }
}

function alert_parameter_delete_1(var1, var2)    //Àà±ðÉèÖÃ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ýÀà±ð£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÀà±ðÂð£¿")) {
        location.assign("./parameter_edit.asp?action=delete&parameter_code=" + var1 + "&img_id=" + var2);
    }
}

function alert_message_delete_1(var1, var2)    //Àà±ðÉèÖÃ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ý¶ÌÐÅ£¬ÇëÈ·ÈÏÉ¾³ý¸Ã¶ÌÐÅÂð£¿")) {
        location.assign("./message_read.asp?action=delete&message_id=" + var1 + "&img_id=" + var2);
    }
}

function alert_file_delete_2(var1, var2)    //·Ö¾ÖÎÄ¼þ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ý¸½¼þ£¬ÇëÈ·ÈÏÉ¾³ý¸Ã¸½¼þÂð£¿")) {
        location.assign("./file_fj_edit.asp?action=file_delete&file_id=" + var1 + "&dir_id=" + var2);
    }
}

function alert_file_fj_delete(var1, var2)    //·Ö¾ÖÎÄ¼þ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ý¸½¼þ£¬ÇëÈ·ÈÏÉ¾³ý¸Ã¸½¼þÂð£¿")) {
        location.assign("./file_fj_edit.asp?action=delete&file_id=" + var1 + "&dir_id=" + var2);
    }
}

function alert_link_delete(var1, var2)    //·Ö¾ÖÎÄ¼þ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ýÁ´½Ó£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÁ´½ÓÂð£¿")) {
        location.assign("./link_edit.asp?action=delete&link_id=" + var1 + "&dir_id=" + var2);
    }
}

function alert_tech_delete_1(var1, var2)    //¾¯½ç·çÔÆ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ýÍ¼Æ¬£¬ÇëÈ·ÈÏÉ¾³ý¸ÃÍ¼Æ¬Âð£¿")) {
        location.assign("./technology_gc_edit.asp?action=file_delete&tech_id=" + var1 + "&img_id=" + var2);
    }
}

function alert_jqjc_delete(var1)    //ÓþÂúÌìÏÂ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸Ã¼ÇÂ¼Âð£¿")) {
        location.assign("./jqjc_edit.asp?action=delete&jqjc_id=" + var1);
    }
}

function alert_admin_delete(var1)    //ÓþÂúÌìÏÂ-ÐÞ¸Ä-É¾³ýÎÄ¼þ
{
    if (confirm("É¾³ý¼ÇÂ¼£¬ÇëÈ·ÈÏÉ¾³ý¸Ã¼ÇÂ¼Âð£¿")) {
        location.assign("./admin_permission_edit.asp?action=delete&admin_id=" + var1);
    }
}

function alert_text(var1) {
    alert(var1);
    window.history.back();
}

function alert_text_n(var1) {
    alert(var1);
}

function insert_img() {
    form1.content.focus();
    var imgstr = prompt("ÇëÊäÈëÍ¼Æ¬Á´½ÓµØÖ·! (ÀýÈç:http://www.xxx.com/abc.jpg)", "http://");
    if (!imgstr == "") {
        document.selection.createRange().text = "[img]" + imgstr + "[/img]\n";
    }
}
function insert_url() {
    form1.content.focus();
    var urlstr = prompt("ÇëÊäÈëÁ´½ÓµØÖ·!(ÀýÈç:http://www.xxx.com/abc.htm))", "http://");
    if (!urlstr == "") {
        var strstr = prompt("ÇëÊäÈëÁ´½ÓÎÄ×ÖËµÃ÷!");
    }
    if (!strstr == "") {
        document.selection.createRange().text = "[url]" + urlstr + "<~@#&/>" + strstr + "[/url]\n";
    }
}

function alert_text_01() {
    alert("±£´æ´íÎó,  ¸Ã±¨±í±¾ÔÂÒÑÌîÐ´,ÇëÈ·¶¨±¨±íÈÕÆÚ£¡");
    window.history.back();
}

function alert_text_02() {
    alert("Êý¾Ý´íÎó,  Ã»ÓÐ²éµ½¸Ã±¨±íÊý¾Ý!");
    window.history.back();
}

function alert_to_reportindex(var1, var2) {
    alert("±£´æÍê³É,  ¸Ã±¨±íÌîÐ´Íê³É£¡");
    location.assign("./index.asp?year_sel=" + var1 + "&month_sel=" + var2);
}

function alert_edit_to_reportindex(var1, var2) {
    alert("±£´æÍê³É,  ¸Ã±¨±íÐÞ¸ÄÍê³É£¡");
    location.assign("./index.asp?year_sel=" + var1 + "&month_sel=" + var2);
}

function alert_doc_add() {
    alert("±£´æÍê³É,  ¸ÃÍ¨ÖªÒÑ·¢²¼£¡");
    location.assign("./report_doc_index.asp");
}

function alert_doc_edit() {
    alert("±£´æÍê³É,  ¸ÃÍ¨ÖªÒÑÐÞ¸ÄÍê³É£¡");
    location.assign("./report_doc_index.asp");
}

function alert_report_add() {
    alert("±£´æÍê³É,  ¸ÃÁÙÊ±±¨±íÒÑ·¢²¼£¡");
    location.assign("./report_temp_index.asp");
}

function alert_report_edit() {
    alert("±£´æÍê³É,  ¸ÃÁÙÊ±±¨±íÒÑÐÞ¸ÄÍê³É£¡");
    location.assign("./report_temp_index.asp");
}

function alert_u_report_add_1() {
    alert("ÁÙÊ±±¨±íÎÄ¼þÉÏ´«Íê³É£¡");
    location.assign("../index_1.asp");
}

function to_report(var1, var2, var3, is_tip) {
    if (is_tip == '0') {
        location.assign("./t_" + var1 + ".asp?year_sel=" + var2 + "&month_sel=" + var3);
    }
    else {
        location.assign("./t_" + var1 + "_brow.asp?year_sel=" + var2 + "&month_sel=" + var3);
    }
}

//×ªÈëä¯ÀÀÒ³Ãæ
function to_report_auditing(var1, var2, var3, is_tip, dept_code) {
    if (is_tip == '1') {
        window.open("./t_" + var1 + "_brow.asp?year_sel=" + var2 + "&month_sel=" + var3 + "&auditing=1&dept_code=" + dept_code, '_blank', 'height=' + (screen.height - 73) + ', width=' + (screen.width - 6) + ',top=-2,left=-2,toolbar=no,menubar=yes,scrollbars=yes,resizable=yes,location=no,status=no');
    }
    else {
        alert('Êý¾Ý´íÎó£¬ ¸Ã±¨±í±¾ÔÂÎ´ÌîÐ´£¡');
    }
}

function report_stat_dept1_sel(var3) {
    var1 = form1.select_dept1.options[form1.select_dept1.selectedIndex].value;
    location.assign("./index.asp?sel_dept=" + var1 + "&sel_reportlist=" + var3);
}

function report_stat_dept2_sel(var3) {
    var2 = form1.select_dept2.options[form1.select_dept2.selectedIndex].value;
    location.assign("./index.asp?sel_dept=" + var2 + "&sel_reportlist=" + var3);
}

function report_stat_reportlist_sel(var1, var2) {
    var3 = form1.select_reportlist.options[form1.select_reportlist.selectedIndex].value;
    location.assign("./index.asp?sel_dept=" + var1 + "&sel_reportlist=" + var3);
}

function menu_show() {
    if (div_menu_1.style.display == "none") {
        div_menu_1.style.display = "block";
    }
    else {
        div_menu_1.style.display = "none";
    }
}

function doc_delete(var1) {
    if (confirm("ÄúÈ·ÈÏÖ´ÐÐÉ¾³ý²Ù×÷Ã´£¿")) {
        location.assign("./report_doc_edit.asp?action=delete&doc_id=" + var1);
    }
}

function doc_add() {
    location.assign("./report_doc_add.asp");
}

function doc_edit(var1) {
    location.assign("./report_doc_edit.asp?doc_id=" + var1);
}

function t_report_add() {
    location.assign("./report_temp_add.asp");
}

function t_report_edit(var1) {
    location.assign("./report_temp_edit.asp?report_id=" + var1);
}

function t_report_delete(var1) {
    if (confirm("ÄúÈ·ÈÏÖ´ÐÐÉ¾³ý²Ù×÷Ã´£¿")) {
        location.assign("./report_temp_edit.asp?action=delete&report_id=" + var1);
    }
}

function t_report_delete2(var1) {
    if (confirm("ÄúÈ·ÈÏÖ´ÐÐÉ¾³ý²Ù×÷Ã´£¿")) {
        location.assign("./report_temp_upload_delete.asp?report_id=" + var1);
    }
}

function t_report_brow() {
    location.assign("./report_temp_upload_brow.asp");
}

function t_report_index() {
    location.assign("./report_temp_index.asp");
}

function t_report_read(var1) {
    location.assign("./report_temp_upload_read.asp?report_id=" + var1);
}

function open_window(var1, var2, var3, var4) {
    window.open(var1, '', 'resizable=' + var4 + ',scrollbars=yes,status=no,toolbar=no,systemmenu=no,location=no,height=' + var3 + ',width=' + var2);
}

function alert_submit_user_delete(var1) {
    if (confirm("ÇëÈ·ÈÏ£¬ÊÇ·ñÉ¾³ý¸ÃÓÃ»§ÐÅÏ¢?")) {
        location.assign("./index_admin_01_delete.asp?user_n=" + var1);
    }
}

function page_jump(var1) {
    var2 = document.all["page_j"].value;
    if (isNaN(parseInt(var2))) {
        return;
    }
    location.assign(var1 + var2 + ".asp");
}

function page_jump_s() {
    var2 = document.all["page_j"].value;
    if (isNaN(parseInt(var2))) {
        return;
    }
    var3 = location.href;
    s_f = var3.indexOf("&page=");
    if (s_f == "-1") {
        location.assign(var3 + "&page=" + var2);
    }
    else {
        location.assign(var3.substring(0, s_f) + "&page=" + var2);
    }
}

function h_02_05() {
    var1 = document.all["h_year"].value;
    if (isNaN(parseInt(var1))) {
        alert('ÇëÊäÈëÄê / ÔÂÊý×Ö£¬Èç£º2008 / 6');
        return;
    }
    var2 = document.all["h_month"].value;
    if (isNaN(parseInt(var2))) {
        alert('ÇëÊäÈëÄê / ÔÂÊý×Ö£¬Èç£º2008 / 6');
        return;
    }
    window.open("./IC_" + var1 + "_" + var2 + ".asp", "_blank");
}