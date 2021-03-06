/*
 *
 *  BlueZ - Bluetooth protocol stack for Linux
 *
 *  Copyright (C) 2018  Intel Corporation. All rights reserved.
 *
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License as published by the Free Software Foundation; either
 *  version 2.1 of the License, or (at your option) any later version.
 *
 *  This library is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Lesser General Public License for more details.
 *
 */

struct mesh_io_private;

typedef bool (*mesh_io_init_t)(struct mesh_io *io, void *opts);
typedef bool (*mesh_io_destroy_t)(struct mesh_io *io);
typedef bool (*mesh_io_caps_t)(struct mesh_io *io, struct mesh_io_caps *caps);
typedef bool (*mesh_io_send_t)(struct mesh_io *io,
					struct mesh_io_send_info *info,
					const uint8_t *data, uint16_t len);
typedef bool (*mesh_io_register_t)(struct mesh_io *io, uint8_t filter_id,
				mesh_io_recv_func_t cb, void *user_data);
typedef bool (*mesh_io_deregister_t)(struct mesh_io *io, uint8_t filter_id);
typedef bool (*mesh_io_filter_set_t)(struct mesh_io *io,
			uint8_t filter_id, const uint8_t *data, uint8_t len,
			mesh_io_status_func_t callback, void *user_data);
typedef bool (*mesh_io_tx_cancel_t)(struct mesh_io *io, const uint8_t *pattern,
								uint8_t len);

struct mesh_io_api {
	mesh_io_init_t		init;
	mesh_io_destroy_t	destroy;
	mesh_io_caps_t		caps;
	mesh_io_send_t		send;
	mesh_io_register_t	reg;
	mesh_io_deregister_t	dereg;
	mesh_io_filter_set_t	set;
	mesh_io_tx_cancel_t	cancel;
};

struct mesh_io {
	enum mesh_io_type		type;
	const struct mesh_io_api	*api;
	struct mesh_io_private		*pvt;
};

struct mesh_io_table {
	enum mesh_io_type		type;
	const struct mesh_io_api	*api;
};
