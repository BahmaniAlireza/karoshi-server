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

function affich_detail_simple($form_name,$list_fields,$list_col_cant_del,$default_fields,$table,$tab_options=array()){
	$form_name="affich_controllers";
	$table_name=$form_name;
	echo open_form($form_name);
//	$list_fields=array($l->g(64) => 'MANUFACTURER',
//					   $l->g(49) => 'NAME',
//					   $l->g(66) => 'TYPE',
//					   'Caption'=>'CAPTION',
//					   $l->g(53)=>'DESCRIPTION',
//					   $l->g(277)=> 'VERSION');
//	//$list_fields['SUP']= 'ID';
//	$list_col_cant_del[$l->g(66)]=$l->g(66);
//	$default_fields= array($l->g(64)=>$l->g(64),$l->g(49)=>$l->g(49),$l->g(66)=>$l->g(66));
	$queryDetails  = "SELECT ";
	foreach ($list_fields as $lbl=>$value){
			$queryDetails .= $value.",";		
	}
	$queryDetails  = substr($queryDetails,0,-1)." FROM ".$table." WHERE (hardware_id=$systemid)";
	tab_req($table_name,$list_fields,$default_fields,$list_col_cant_del,$queryDetails,$form_name,80,$tab_options);
	echo close_form();


}
?>