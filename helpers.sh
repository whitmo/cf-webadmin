function do-relate(){
    for i in nats uaa:uaa cc uaa:uaa-db mysql cloudfoundry;
    do
        juju add-relation $1 $i;
    done
}
