
#####################
# MODULE : test.pm
#####################
sub init_test{
	$hooks{'test'} = '&test_dosomething;';
	}

sub test_dosomething{
    print "I am doing something right here";
    }
return 1;