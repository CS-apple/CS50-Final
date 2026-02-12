SELECT
	orders.order_id, 
	user.first_name, 
	user.last_name, 
	user.email, 
	user.phone, 
	orders.total, 
	orders.pickup_date, 
	orders.status_code, 
	(
		SELECT GROUP_CONCAT ( boxes.quantity || 'x ' || doughnuts.doughnut_name, ' | ') 
		FROM order_items 
		INNER JOIN boxes ON boxes.order_details = order_items.detail_id 
		INNER JOIN doughnuts ON boxes.items = doughnuts.doughnut_id 
		WHERE order_items.order_id = orders.order_id 
	) AS items 
FROM orders 
INNER JOIN user ON orders.user = user.user_id 
WHERE orders.status_code < 3 
GROUP BY orders.order_id 
ORDER BY orders.pickup_date 
LIMIT 20;