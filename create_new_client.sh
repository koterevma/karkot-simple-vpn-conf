#!/usr/bin/env bash

[[ "$EUID" -ne 0 ]] && echo "Please, run with \"sudo $0\"" && exit

config_dir=/etc/wireguard_client_confs
given_ips_file=$config_dir/given_ips
last_given_ip=$(tail -n1 $given_ips_file | awk '{print $1}')

new_address=$(echo $last_given_ip | awk -F. '{printf("%d.%d.%d.%d", $1, $2, $3, $4 + 1)}')
echo "$new_address will be given to new client (last was $last_given_ip)"

read -p "Enter new config name: " new_connection_name

new_conf_name=$new_connection_name".conf"
read -p "New config \"$config_dir/$new_conf_name\" will be created (Enter to continue, Ctrl^C to cancel)"

new_generated_public_key=$(wg genkey | tee /etc/wireguard/${new_connection_name}_privatekey | wg pubkey > /etc/wireguard/${new_connection_name}_publickey)

chmod 600 /etc/wireguard/${new_connection_name}_privatekey

cp $config_dir/template.conf $config_dir/$new_conf_name
private_key=$(< /etc/wireguard/${new_connection_name}_privatekey)
sed -i 's/PRIVATE_KEY/'"$private_key"'/;s/ADRESS_TO_GIVE/'"$new_address"'/' $config_dir/$new_conf_name

echo "
[Peer]
PublicKey = $new_generated_public_key
AllowedIPs = $new_address/32" >> /etc/wireguard/wg0.conf

systemctl restart wg-quick@wg0.service
systemctl status wg-quick@wg0.service

qrencode -o $config_dir/qr_$new_connection_name.png -r $config_dir/$new_conf_name
echo $new_conf_name was created! Check auto-generated qr-code here: $config_dir/qr_$new_connection_name.png

echo "To copy it from server for example use \"scp vpn_server:$config_dir/qr_$new_connection_name.png /mnt/c/Users/<USER>/qr_$new_connection_name.png\""

echo $new_address $new_conf_name >> $given_ips_file

