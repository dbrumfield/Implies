#!/usr/bin/perl

use CGI;
use DBI;

print "content-type: text/plain\n\n";

$q=new CGI;

$ASCIIName = $q->param('ASCIIName') || $ARGV[0];
$LaTexName = $q->param('LaTexName') || $ARGV[1];
$Reference = $q->param('Reference') || $ARGV[2];
$FreeText = $q->param('FreeText')   || $ARGV[3];
$Overwrite = $q->param('Overwrite') || $ARGV[4] || 0;

my $date = `/bin/date`;
chomp $date;
open MYFILE, '>>', "/tmp/log.txt" or die $!;
print MYFILE "$date $ASCIIName\t $LaTexName\t $Reference\t $FreeText\n";
close MYFILE;

my $dbh=DBI->connect("DBI:mysql:database=Zoo;mysql_read_default_file=/home/mummertc/.my.cnf", "", "", {'AutoCommit'=>0});

$sql = "select * from Subsystems where sub_Ascii = ?";  # because sub_Ascii is a unique key
$sh = $dbh->prepare($sql);
$c = $sh->execute($ASCIIName);
$sh->finish();

if ( $c == 0) { 
  # insert
  $sql = "INSERT INTO Subsystems VALUES(?, ?, ?, ?)";

  $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
  my $c = $sth->execute($ASCIIName, $LaTexName, $Reference, $FreeText);
  print "Success\n";
} else { 
  if ( 1 == $Overwrite ) { 
    # update the row

     # ... 

    print "Success\n";
  } else { 
    # it's a duplicate, send error
    print "Duplicate\n";
  }
}


$dbh->disconnect();

