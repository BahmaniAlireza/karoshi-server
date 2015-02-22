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

/*
 * 
 * Show sd_modems data
 * 
 * 
 */
print_item_header($l->g(1266));
	if (!isset($protectedPost['SHOW']))
		$protectedPost['SHOW'] = 'NOSHOW';
	$table_name="snmp_virtualmachines";

   $list_fields=array($l->g(137)=>'CONFIG_FILE',
                  $l->g(54) => 'CPU',
                  $l->g(23)=>'NAME',
                  $l->g(26)=>'MEMORY',
                  $l->g(25)=>'OS',
                  $l->g(6005)=>'POWER',
                  $l->g(1268)=>'UUID');
	$sql=prepare_sql_tab($list_fields);
	$list_col_cant_del=$list_fields;
	$default_fields= $list_fields;
	$sql['SQL']  = $sql['SQL']." FROM %s WHERE (snmp_id=%s)";
	$sql['ARG'][]='snmp_virtualmachines';
	$sql['ARG'][]=$systemid;
	$tab_options['ARG_SQL']=$sql['ARG'];
	tab_req($table_name,$list_fields,$default_fields,$list_col_cant_del,$sql['SQL'],$form_name,80,$tab_options);


?>
