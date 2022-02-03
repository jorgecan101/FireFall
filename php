<!DOCTYPE html>
<head>
<title>Insert data to PostgreSQL with php - creating a simple web application</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style>
li {listt-style: none;}
</style>
</head>
<body>
<h2>Enter information regarding book</h2>
<ul>
<form name="insert" action="insert.php" method="POST" >
<li>Book ID:</li><li><input type="text" name="bookid" /></li>
<li>Book Name:</li><li><input type="text" name="book_name" /></li>
<li>Author:</li><li><input type="text" name="author" /></li>
<li>Publisher:</li><li><input type="text" name="publisher" /></li>
<li>Date of publication:</li><li><input type="text" name="dop" /></li>
<li>Price (USD):</li><li><input type="text" name="price" /></li>
<li><input type="submit" /></li>
</form>
</ul>
</body>
</html>
<?php
$db = pg_connect("host=localhost port=5432 dbname=postgres user=postgres password=admin123");
$query = "INSERT INTO book VALUES ('$_POST[bookid]','$_POST[book_name]',
'$_POST[author]','$_POST[publisher]','$_POST[dop]',
'$_POST[price]')";
$result = pg_query($query); 
?>


<?php
try {$dbuser = 'hackutd';
$dbpass = 'hackutd2019';
$host = '69.164.204.53';
$dbname='hackutd';
$connec = pg_connect("host=localhost port=5432 dbname=hackutd user=hackutd password=admin123");
}catch (PDOException $e) {
echo "Error : " . $e->getMessage() . "<br/>";
die();
}
$sql = 'SELECT fname, lname, country FROM user_details ORDER BY country';
foreach ($connec->query($sql) as $row) 
{
print $row['fname'] . " ";
print $row['lname'] . "-->";
print $row['country'] . "<br>";
}
?>
