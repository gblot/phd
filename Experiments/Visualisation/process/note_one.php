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
		
	if(isset($_GET["csv"]) && isset($_GET["channel"])) {
		
		$csv 			= $_GET["csv"];		// our CSV file
		$channel 		= $_GET["channel"];	// the channel we want to extract
		$channel_found 	= false;			// boolean giving information ifthe requested channel exists
		
		
		$fp = fopen($csv.".csv", "r"); 		// Read the CSV file

		$fp_w = fopen($csv."_".$channel.".q.notes", 'w');	// Prepare the output csv file
		fwrite($fp_w, "Beat\t0\t200");
		fwrite($fp_w, "\r\n");	

		$doc = array();

		if($fp){

			while (!feof($fp)) { // going through CSV the file
				
				$ligne = fgets($fp, 4096);		// get the following line;				
				$doc[] = $ligne;

			}

			$last = 0;

			for($i=0;$i<sizeof($doc);$i++){

				$tmp_i = explode(",",$doc[$i]);

				if($tmp_i[3]==$channel){			// check if we are in the requested channel

					if(trim($tmp_i[2])=="Note_on_c" && (int)$tmp_i[5]){			// check if it an ON_NOTE event

						$found_note = trim($tmp_i[4]);

						for($j=$i;$j<sizeof($doc);$j++){
						
							$tmp_j = explode(",",$doc[$j]);

							if((trim($tmp_j[2])=="Note_off_c" || (trim($tmp_j[2])=="Note_on_c"  && !(int)$tmp_j[5])) && $tmp_j[4]==$found_note){

								fwrite($fp_w, "Note\t".$tmp_i[1]."\t".$tmp_j[1]."\t".$found_note);
								fwrite($fp_w, "\r\n");	
								
								$last = $tmp_j[1];

								break;
							}
						}
					}

					$channel_found = true;
				}
			}

		} else echo "ERROR_1: Please, give a csv filename as an argument (?csv=)."; 

		if(!$channel_found) echo "ERROR_2: INVALID Channel argument";

	} else echo "ERROR_3: Please, give a csv filename (?csv=) and a track channel (&channel=)"; 

	fwrite($fp_w, "Beat\t".$last."\t200");
	fwrite($fp_w, "\r\n");	
	
	// close the streams
	fclose($fp);
	fclose($fp_w);

?>