<?php
//====================================================================================
// OCS INVENTORY REPORTS
// Copyleft Erwan GOALOU 2010 (erwan(at)ocsinventory-ng(pt)org)
// Web: http://www.ocsinventory-ng.org
//
// This code is open source and may be copied and modified as long as the source
// code is always made freely available.
// Please refer to the General Public Licence http://www.gnu.org/ or Licence.txt
//====================================================================================

require_once('require/function_search.php');
require_once('require/function_users.php');

if (isset($protectedPost['Reset_modif_x'])){
	unset($protectedPost['MODIF']);
}

 //d�finition des onglets
$list_profil=search_profil();
$data_on=$list_profil;
$data_on[4]=$l->g(244);

if ($_SESSION['OCS']['CONFIGURATION']['MANAGE_PROFIL'] == 'YES')
	$data_on[5]=$l->g(1146);

$form_name = "admins";
echo open_form($form_name);
onglet($data_on,$form_name,"onglet",4);
$table_name="TAB_ACCESSLVL".$protectedPost['onglet'];	
if ($protectedPost['onglet'] != $protectedPost['old_onglet']){
unset($protectedPost['MODIF']);
}

if ($protectedPost['onglet']==""){
	$protectedPost['onglet'] = current($data_on);
}

//suppression d'une liste de users
if (isset($protectedPost['del_check']) and $protectedPost['del_check'] != ''){
	delete_list_user($protectedPost['del_check']);
	$tab_options['CACHE']='RESET';	
}

//suppression d'un user
if (isset($protectedPost['SUP_PROF']) and $protectedPost['SUP_PROF'] != ''){
	delete_list_user($protectedPost['SUP_PROF']);	
	$tab_options['CACHE']='RESET';
}

//ajout d'un user
if (isset($protectedPost['Valid_modif_x'])){
	$ok=add_user($protectedPost,$list_profil);
	if ($ok == $l->g(373) or $ok == $l->g(374)){
		unset($_SESSION['OCS']['DATA_CACHE'],$protectedPost['ID'],$protectedPost['FIRSTNAME'],$protectedPost['LASTNAME'],
		$protectedPost['ACCESSLVL'],$protectedPost['COMMENTS'],$protectedPost['PASSWORD'],$protectedPost['MODIF']);
		$tab_options['CACHE']='RESET';	
		msg_success($ok);
	}else
		msg_error($ok);
	
}
echo '<div class="mlt_bordure" >';
//add user or modif
if ($protectedPost['onglet'] == 4 
	or (isset($protectedPost['MODIF']) and $protectedPost['MODIF'] != '')){	
	admin_user($protectedPost['MODIF']);

}elseif ($protectedPost['onglet'] == 5 and $_SESSION['OCS']['CONFIGURATION']['MANAGE_PROFIL'] == 'YES'){
	admin_profil($form_name);
}
else{
	echo "<tr><td align=center>";
	//affichage
	$list_fields= array('ID'=>'ID',
						$l->g(49)=>'FIRSTNAME',
						$l->g(996)=>'LASTNAME',
						$l->g(66)=>'NEW_ACCESSLVL',
						$l->g(51)=>'COMMENTS',
						$l->g(1117)=>'EMAIL',
						$l->g(607)=>'USER_GROUP',
						'SUP'=>'ID',
						'MODIF'=>'ID',
						'CHECK'=>'ID');
	$list_col_cant_del=array('ID'=>'ID','SUP'=>'SUP','MODIF'=>'MODIF','CHECK'=>'CHECK');
	$default_fields=$list_fields; 
	$queryDetails = 'SELECT ';
	foreach ($list_fields as $key=>$value){
		if($key != 'SUP' and $key != 'MODIF' and $key != 'CHECK')
		$queryDetails .= $value.',';		
	} 
	$queryDetails=substr($queryDetails,0,-1);
	$queryDetails .= " FROM operators where NEW_ACCESSLVL='".$protectedPost['onglet']."'";
	$tab_options['FILTRE']=array('LASTNAME'=>'LASTNAME','ID'=>'ID');
		$tab_options['LIEN_LBL']['ID']='index.php?'.PAG_INDEX.'='.$pages_refs['ms_custom_perim'].'&head=1&id=';'admin_perim.php?id=';
		$tab_options['LIEN_CHAMP']['ID']='ID';
		$tab_options['LIEN_TYPE']['ID']='POPUP';
		$tab_options['POPUP_SIZE']['ID']="width=550,height=650";
	$sql_user_groups="select IVALUE,TVALUE from config where name like 'USER_GROUP_%' ";
	$res_user_groups = mysql_query( $sql_user_groups, $_SESSION['OCS']["readServer"] );
	while ($val_user_groups = mysql_fetch_array( $res_user_groups ))
	$user_groups[$val_user_groups['IVALUE']]=$val_user_groups['TVALUE'];

	$tab_options['REPLACE_VALUE'][$l->g(607)]=$user_groups;
	$tab_options['LBL']['SUP']=$l->g(122);
	$tab_options['LBL']['MODIF']=$l->g(1118);
	$tab_options['LBL']['CHECK']=$l->g(1119);
	tab_req($table_name,$list_fields,$default_fields,$list_col_cant_del,$queryDetails,$form_name,100,$tab_options);
		//traitement par lot
	$img['image/sup_search.png']=$l->g(162);
	del_selection($form_name);
}
echo '</div>';
echo close_form();
?>
