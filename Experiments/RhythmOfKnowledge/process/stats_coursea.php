<?PHP

	// Course B
	//$file = "coursea1.gexf";
	//$file = "coursea2.gexf";
	$file = "coursea3.gexf";

	// Lessons composition
	$lessons = array(55, 75, 79, 80, 81, 83, 82, 54,78,77, 76, 72, 71, 70 ,69, 68, 67, 66, 65 ,64, 63, 62, 61 , 60, 59, 58, 57, 56, 42, 41, 40, 39, 38 , 37, 9, 36, 35 , 34, 33, 32, 31, 30, 29);

	// Exercises composition
	$exercise = array(50, 53,
		48, 74, 52, 51,
		46, 73, 47,45,
		43, 84, 28, 44,
		49, 88, 86, 85,
		27, 20, 26, 25,
		24, 23, 22, 21,
		19, 18, 17, 16, 15, 14,
		13, 12, 10, 11,
		87,
		7, 8,
		6, 5,
		1, 4,
		3, 2);

	// Sections compositions
	$sections = array();
	$sections[] = array(55, 75, 79, 80, 50, 53);
	$sections[] = array(81, 83, 82, 48, 74, 52, 51);
	$sections[] = array(54,78,77, 76, 46, 73, 47,45);
	$sections[] = array(72, 71, 70, 43, 84, 28, 44);
	$sections[] = array(69, 68, 67, 66, 65, 49, 88, 86, 85);
	$sections[] = array(64, 63, 27, 20, 26, 25);
	$sections[] = array(62, 61, 24, 23, 22, 21);
	$sections[] = array(60, 59, 58, 57, 56, 19, 18, 17, 16, 15, 14);
	$sections[] = array(42, 41, 40, 39, 38, 13, 12, 10, 11);
	$sections[] = array(37, 9, 87);
	$sections[] = array(36, 35, 7, 8); 
	$sections[] = array(34, 33, 32, 6, 5);
	$sections[] = array(31, 1, 4);
	$sections[] = array(30, 29, 3, 2);

	$doc = new DomDocument();
	$doc->load($file);

	$ALLNODES = array();
	$nodes = $doc->getElementsByTagName('node');
	foreach($nodes as $node) {
		$ALLNODES[] = $node->getAttribute("id");
	}

	$density_lessons = array();
	$density_exercises = array();
	$density_lessons_oriented = array();
	$density_exercises_oriented = array();
	$ex_ex = array();
	$ex_le = array();
	$le_le = array();
	$le_ex = array();
	$inte_ex_ex = array();
	$inte_ex_le = array();
	$inte_le_le = array();
	$inte_le_ex = array();
	$inte_all = array();
	for($i=0;$i<sizeof($ALLNODES);$i++){
		$dens_l = 0;
		$dens_e = 0;
		$dens_lo = 0;
		$dens_eo = 0;
		$rat_ex_ex = 0;
		$rat_ex_le = 0;
		$rat_le_le = 0;
		$rat_le_ex = 0;
		$edges = $doc->getElementsByTagName('edge');
		foreach($edges as $edge){
			if($edge->getAttribute('source')==$ALLNODES[$i]){

				$inte_all[]=$edge->getAttribute('weight');

				// directed
				if(in_array($edge->getAttribute('source'), $exercise)){
					if(in_array($edge->getAttribute('target'), $exercise)){
						$dens_eo++;
						$dens_e++;
						$rat_ex_ex++;
						$inte_ex_ex[]=$edge->getAttribute('weight');
					} else {
						$rat_ex_le++;
						$inte_ex_le[]=$edge->getAttribute('weight');
					}
				} else {
					if(in_array($edge->getAttribute('target'), $lessons)){
						$dens_lo++;
						$dens_l++;
						$rat_le_le++;
						$inte_le_le[]=$edge->getAttribute('weight');
					} else {
						$rat_le_ex++;
						$inte_le_ex[]=$edge->getAttribute('weight');
					}
				}

				// if undirected
				if(in_array($edge->getAttribute('target'), $exercise)){
					if(in_array($edge->getAttribute('source'), $exercise)){
						$dens_e++;
					}
				} else {
					if(in_array($edge->getAttribute('source'), $lessons)){
						$dens_l++;
					}
				}
			}
		}

		if(in_array($ALLNODES[$i], $lessons)) $density_lessons_oriented[] = $dens_lo;
		else $density_exercises_oriented[] = $dens_eo;

		$ex_ex[] = $rat_ex_ex/($rat_ex_ex+$rat_ex_le);
		$le_le[] = $rat_le_le/($rat_le_le+$rat_le_ex);

	}

	function getDiameter($nodes,$edges,$arr){

		$wholepath = array();
		foreach($nodes as $node){
			if(in_array($node->getAttribute("id"),$arr)){
				$ID = $node->getAttribute("id");
				for($j=0;$j<sizeof($arr);$j++){
					if($arr[$j]!=$ID){
						// BFS
						$visited = array();
						$start = $ID;
					    $q = array();
					    array_push($q, $start);						
					    $visited[$start] = 1;
					    //echo $start . "\n";
					    $found = false;
					    $cpt = 0;
					    while (count($q)) {
					        $t = array_shift($q);
					        $cpt++;
					 		foreach($edges as $edge){
					 			if($edge->getAttribute("source")==$t && in_array($edge->getAttribute("target"),$arr) && $visited[$edge->getAttribute("target")]!=1){
					 				$visited[$edge->getAttribute("target")] = 1;
					 				array_push($q, $edge->getAttribute("target"));
					 				if($edge->getAttribute("target")==$arr[$j]){
					 					$found = true;
					 					break;
					 				}
					 			}
					 		}
					 		if($found) break;
					 		if($cpt>2) break;
					    }		
					    $wholepath[] = $cpt;			    
					}
				}
			}
		}

		echo max($wholepath)." ".array_sum($wholepath)/sizeof($wholepath)."<br/>";
	}

	$sections_ratio = array();
	$sections_dens = array();
	$sections_dens_u = array();
	$sections_int = array();

	for($j=0;$j<sizeof($sections);$j++){
		$cpt_sec_u = 0;
		$cpt_sec = 0;
		$cpt = 0;
		$cpt_int = 0;
		foreach($edges as $edge){
			if(in_array($edge->getAttribute('source'), $sections[$j])){
				if(in_array($edge->getAttribute('target'), $sections[$j])){
					$cpt_sec++;
					$cpt_sec_u++;
					$cpt++;
					$cpt_int+=$edge->getAttribute('weight');
				} else {
					$cpt++;
				}
			}
		}

		$sections_ratio[] = $cpt_sec/$cpt;
		$sections_dens[] = $cpt_sec/(sizeof($sections[$j])*(sizeof($sections[$j])-1)); 
		$sections_int[] = $cpt_int/$cpt_sec_u;

		// getDiameter($nodes,$edges,$sections[$j]);

	}

	// getDiameter($nodes,$edges,$lessons);
	// getDiameter($nodes,$edges,$exercise);

	$full_l = array_sum($density_lessons_oriented)/(sizeof($lessons)*(sizeof($lessons)-1));
	$full_e = array_sum($density_exercises_oriented)/(sizeof($exercise)*(sizeof($exercise)-1));

	for($i=0;$i<sizeof($density_lessons_oriented);$i++){
		$density_lessons_oriented[$i] = $density_lessons_oriented[$i]/(sizeof($lessons)-1);
	}

	for($i=0;$i<sizeof($density_exercises_oriented);$i++){
		$density_exercises_oriented[$i] = $density_exercises_oriented[$i]/(sizeof($exercise)-1);
	}

	sort($inte_all);
	echo "OVERALL:<br/>";
	echo "AVG Interval ".(round(array_sum($inte_all)/sizeof($inte_all))/3600)." hours<br/>";
	echo "Median Interval ".round($inte_all[(int)(sizeof($inte_all)/2)])." sec <br/>";

	echo "<br>SECTIONS:<br/>";
	echo "Density ".round(array_sum($sections_dens)/sizeof($sections_dens),3)."<br/>";
	echo "Interval ".(round(array_sum($sections_int)/sizeof($sections_int))/3600)." hours<br/>";

	$cpt = 1;
	echo "<div style='margin:0px 20px';>";
	for($i=0;$i<sizeof($sections_dens);$i++){
		echo "sec ".$cpt." (".round($sections_dens[$i],3)." / ".round($sections_int[$i])."sec)<br/>";
		$cpt++;
	}
	echo "</div>";


	echo "<br>LESSONS:<br/>";
	echo "Amount ".sizeof($lessons)."<br/>";
	echo "Density ".round(array_sum($density_lessons_oriented)/sizeof($density_lessons_oriented),3)."<br/>";
	$int = round(array_sum($inte_le_le)/sizeof($inte_le_le));
	echo "Interval ".($int/3600)." hours<br/>";
	echo "Ratio ".round(array_sum($ex_ex)/sizeof($ex_ex),2)."<br/>";

	echo "<br>EXERCISES:<br/>";
	echo "Amount ".sizeof($exercise)."<br/>";
	echo "Density ".round(array_sum($density_exercises_oriented)/sizeof($density_exercises_oriented),3)."<br/>";
	$int = round(array_sum($inte_ex_ex)/sizeof($inte_ex_ex));
	echo "Interval ".($int/3600)." hours<br/>";
	echo "Ratio ".round(array_sum($le_le)/sizeof($le_le),3)."<br/>";

	echo "<br>OTHER:<br/>";	
	echo "ex to le avg. Int ".((round(array_sum($inte_ex_le)/sizeof($inte_ex_le)))/3600)." hours<br/>";
	echo "le to ex avg. Int ".((round(array_sum($inte_le_ex)/sizeof($inte_le_ex)))/3600)." hours<br/>";
	


?>