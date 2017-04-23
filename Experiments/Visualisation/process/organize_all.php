<?php

	/* 
		This program parses a CSV file imported by the MIDI to CSV program (http://www.fourmilab.ch/webtools/midicsv/) 
		and produces a readable log file of notes events for a given channel.

		It needs 2 GET arguments:
			- csv: the CSV file (imported with MIDI to CSV)

		if you want to log all channels please refer to allchannel.php
	*/

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


	// Check if valid arguments
	if(isset($_GET["csv"])) {
		
		$csv 			= $_GET["csv"];		// our CSV file
		$excl			= explode(";",$_GET["exclusion"]);		// channels to exclude (usually drums)
		
		$fp = fopen($csv.".csv", "r"); 		// Read the CSV file

		$fp_w = fopen($csv."_all_log.csv", 'w');	// Prepare the output csv file
		fwrite($fp_w, '"time","item","user"');
		fwrite($fp_w, "\r\n");	

		$csv_output 	= array();
		$output_order	= array();

		if($fp){

			while (!feof($fp)) { // going through CSV the file
				
				$ligne = fgets($fp, 4096);		// get the following line;
				$tmp = explode(",",$ligne);		// put the line in an arry

				if(!in_array($tmp[3],$excl)){	// check if we are in the requested channel
				
					if(trim($tmp[2])=="Note_on_c" && (int)$tmp[5]){			// check if it an ON_NOTE event

						$note = (int)trim($tmp[4])%12;		// collect the pitch of the note on the octave

						$csv_output[] = trim($tmp[1]).",".$note.",".$tmp[3];
						$output_order[] = trim($tmp[1]); 
			
					}

				}

				$channel_found = true;		// we found the requested channel

			}

			$csv_output = sortarray($csv_output,$output_order);

			foreach ($csv_output as $key => $value) {
				fwrite($fp_w, $value);
				fwrite($fp_w, "\r\n");
			}

		} else echo "ERROR_1: Please, give a csv filename as an argument (?csv=)."; 


	} else echo "ERROR_3: Please, give a csv filename (?csv=)"; 
	
	// close the streams
	fclose($fp);
	fclose($fp_w);

	echo 'OK';

?>