#!/usr/bin/perl
use CGI qw(:all);
print header;
################################################################################
#### VARIABLES
################################################################################
$module_error = "";
################################################################################
### ANALYZE QUERY STRING
### All the values coming from the browser are passed to the array $form
################################################################################
$query=$ENV{'QUERY_STRING'};
if ($query){
    @pairs=split(/&/,$query);
    } else {
    read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    @pairs = split(/&/, $buffer);
    }
foreach $pair (@pairs) {
    $something_in=1; ($name, $value) = split(/=/, $pair);
    $value =~ tr/+/ /; $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $name =~ tr/+/ /; $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    if ($form{$name}) { $form{$name} = $form{$name}.",".$value; } else { $form{$name} = $value; }
    $form{$name} =~ s/'/''/g;
    }
################################################################################
#### LOADS AND INITIALIAZES ALL THE PLUGINS IN THE DIRECTORY
#### all plugins to have extension ".pm"
################################################################################
if ( $ENV{'HTTPS'} eq "on" ){
    $var_http = "https";
    } else {
    $var_http = "http";
    }
$plugin_directory = './plugins';
$var_script = "$var_http://$ENV{'SERVER_NAME'}$ENV{'SCRIPT_NAME'}";
################################################################################
use lib ('plugins');
opendir (DIR, $plugin_directory) or die $!;
while (my $file = readdir(DIR)) {
    next unless ($file =~ m/(.*?)\.pm$/);
    push(@modules,$1);
    }
closedir(DIR);
foreach $module (@modules){
    eval "require $module";
    &{"init_$module"};
    if ($module_error ne "") { 
        print "$module_error"; 
        }
    }
################################################################################
### Events Management
################################################################################
if ( $hooks{"$form{'action'}"}) { 
    eval $hooks{"$form{'action'}"} 
    } else { 
    &main;
    }
exit;
################################################################################
#### TRAPS ANY NON EXISTING OR WRONG SUB RETURNING THE NAME IN module_error
################################################################################
sub AUTOLOAD {
    use vars qw($AUTOLOAD);
    my $error = $AUTOLOAD;
    $error =~ s/.*:://;
    $module_error = "$error";
    }