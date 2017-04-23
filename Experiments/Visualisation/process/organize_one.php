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

		$fp_w = fopen($csv."_".$channel."_log.csv", 'w');	// Prepare the output csv file
		fwrite($fp_w, '"time","item","user"');
		fwrite($fp_w, "\r\n");	

		$csv_output = array();

		if($fp){

			while (!feof($fp)) { // going through CSV the file
				
				$ligne = fgets($fp, 4096);		// get the following line;
				$tmp = explode(",",$ligne);		// put the line in an arry
				
				if($tmp[3]==$channel){			// check if we are in the requested channel

					if(trim($tmp[2])=="Note_on_c" && (int)$tmp[5]){	// check if it an ON_NOTE event

						$note = (int)trim($tmp[4])%12;		// collect the pitch of the note on the octave

						// Write a new log
						//fwrite($fp_w, trim($tmp[1]).",".$note.",".$channel);
						//fwrite($fp_w, "\r\n");	

						$csv_output[] = trim($tmp[1]).",".$note.",".$channel;
			
					}

					$channel_found = true;		// we found the requested channel

				}

			}

			$csv_output = array_reverse($csv_output);

			foreach ($csv_output as $key => $value) {
				fwrite($fp_w, $value);
				fwrite($fp_w, "\r\n");
			}

		} else echo "ERROR_1: Please, give a csv filename as an argument (?csv=)."; 

		if(!$channel_found) echo "ERROR_2: INVALID Channel argument";

	}
	else echo "ERROR_3: Please, give a csv filename (?csv=) and a track channel (&channel=)"; 
	
	// close the streams
	fclose($fp);
	fclose($fp_w);

?>