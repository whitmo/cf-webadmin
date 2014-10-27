function cfwa-relate(){
    for i in nats uaa:uaa cc uaa:uaa-db mysql cloudfoundry;
    do
        juju add-relation cf-webadmin $i;
    done
}
