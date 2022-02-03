<html>

  <head>
   <title>Test</title>
  </head>

  <body bgcolor="white">

  <?


  $link = pg_connect("host=69.164.204.53 port=5432 dbname=hackutd user=hackutd password=admin123");
  $result = pg_exec($link, "select id, zipcode, risk_score from zipcode");
  $numrows = pg_numrows($result);
  echo "<p>link = $link<br>
  result = $result<br>
  numrows = $numrows</p>
  ";
  ?>

  <table border="1">
  <tr>
   <th>id</th>
   <th>zipcode</th>
   <th>risk_score</th>
  </tr>
  <?

   // Loop on rows in the result set.

   for($ri = 0; $ri < $numrows; $ri++) {
    echo "<tr>\n";
    $row = pg_fetch_array($result, $ri);
    echo " <td>", $row["id"], "</td>
   <td>", $row["zipcode"], "</td>
   <td>", $row["risk_score"], "</td>
  </tr>
  ";
   }
   pg_close($link);
  ?>
  </table>

  </body>

  </html>


  try {$dbuser = 'hackutd';
$dbpass = 'hackutd2019';
$host = '69.164.204.53';
$dbname='hackutd';