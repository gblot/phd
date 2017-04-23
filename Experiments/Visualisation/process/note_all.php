<?php

	/* 
		This program parses a CSV file imported by the MIDI to CSV program (http://www.fourmilab.ch/webtools/midicsv/) 
		and produces a readable log file of notes events for a given channel.

		It needs 2 GET arguments:
			- csv: the CSV file (imported with MIDI to CSV)
			- channel: the channel you want to log

		if you want to log all channels please refer to allchannel.php
	*/

	// Check if valid arguments

	function sortarray($outarray,$seed) {

		$sorted_array = array();
		$cpt = 0;

		do{

			$value = false;
			
			$swap = -1;
			$swap_index = -1;
			
			for($j=0;$j<sizeof($seed);$j++){

				if($swap<(int)$seed[$j]){
					$swap=(int)$seed[$j];
					$swap_index=$j;

					$value = true;
				}
			
			}

			if($value){
				$sorted_array[] = $outarray[$swap_index];
				array_splice($seed, $swap_index, 1, -2);				
			}
						
		} while($value);

		return $sorted_array;

	}
		
	if(isset($_GET["csv"]) && isset($_GET["channel"])) {
		
		$csv 			= $_GET["csv"];		// our CSV file
		$channel 		= $_GET["channel"];	// the channel we want to extract
		$channel_found 	= false;			// boolean giving information ifthe requested channel exists

		$excl			= explode(";",$_GET["exclusion"]);		// channels to exclude (usually drums)		
		
		$fp = fopen($csv.".csv", "r"); 		// Read the CSV file

		$fp_w = fopen($csv.".all.q.notes", 'w');	// Prepare the output csv file
		fwrite($fp_w, "Beat\t0\t200");
		fwrite($fp_w, "\r\n");	

		$doc = array();
		$csv_output 	= array();
		$output_order	= array();

		if($fp){

			while (!feof($fp)) { // going through CSV the file
				
				$ligne = fgets($fp, 4096);		// get the following line;				
				$doc[] = $ligne;

			}

			$last = 0;

			for($i=0;$i<sizeof($doc);$i++){

				$tmp_i = explode(",",$doc[$i]);

				if(!in_array($tmp_i[3],$excl)){	// check if we are in the requested channel

					if(trim($tmp_i[2])=="Note_on_c" && (int)$tmp_i[5]){			// check if it an ON_NOTE event

						$found_note = trim($tmp_i[4]);

						for($j=$i;$j<sizeof($doc);$j++){
						
							$tmp_j = explode(",",$doc[$j]);
							if((trim($tmp_j[2])=="Note_off_c" || (trim($tmp_j[2])=="Note_on_c"  && !(int)$tmp_j[5])) && $tmp_j[4]==$found_note){
		
								$csv_output[] = "Note\t".$tmp_i[1]."\t".$tmp_j[1]."\t".$found_note;
								$output_order[] = trim($tmp_i[1]);
								
								if($tmp_j[1]>$last) $last = $tmp_j[1];

								break;
							}
						}
					}
				}

				$channel_found = true;
	
			}

				$csv_output = array_reverse(sortarray($csv_output,$output_order));

				foreach ($csv_output as $key => $value) {
					fwrite($fp_w, $value);
					fwrite($fp_w, "\r\n");
				}

		} else echo "ERROR_1: Please, give a csv filename as an argument (?csv=)."; 

		if(!$channel_found) echo "ERROR_2: INVALID Channel argument";

	} else echo "ERROR_3: Please, give a csv filename (?csv=) and a track channel (&channel=)"; 

	fwrite($fp_w, "Beat\t".$last."\t200");
	fwrite($fp_w, "\r\n");	
	
	// close the streams
	fclose($fp);
	fclose($fp_w);

	echo 'OK';

?>