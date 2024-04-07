# MCFS

Author: `tacex`

The size of a Minecraft world is 60,000,000 * 60,000,000 * 384 blocks. If 256 different blocks are chosen to represent a byte of data, this means that a Minecraft world could store roughly 1.2 exabytes of data. Naturally, this must mean that Minecraft is the best storage system in terms of capacity, so I have decided to start storing my files in my world. Have fun recovering them!

Note: The file size is 8MB

Download from here: https://tamuctf.com/5d6b407ee061e8696136d4dfd25f24b0/static/mcfs.zip

## Solution

The first step to solving this challenge is reversing the JAR used to place the file into the world. To get the class files from the JAR, `mcfs.jar` can be unzipped. Then, jadx was used to recover the java source code from `MCFS.class` and `CommandWrite.class`. Using this information, it is clear that the best course of action to recover the flag is to write your own plugin. 

It is possible to determine that the original JAR was written with spigot, but it is not necessary to solve with spigot since the world file can be used with any other server. Additionally, hosting a server is free and plugin commands can be run from the server CLI, so a Minecraft account is not needed to solve.

I ended up writing a plugin using spigot and reusing alot of the code from the JAR to get the block mappings and then read the blocks to a file. I wrote the values as decimal to a file because I couldn't be bother to deal with converting to bytes. Then, I just used python to convert the ascii values into the original file.

```java
package com.tamuctf.mina_filer;

import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.List;

import org.bukkit.Material;
import org.bukkit.Tag;
import org.bukkit.block.Block;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.command.CommandExecutor;

public class CommandReadFile implements CommandExecutor {
	public static final int CHUNKSIZE = 16;
	public static final int CHUNKHEIGHT = 256;
	public static final int BLOCKLEN = 16;
	
	@Override
	public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
		if(args.length != 5)
			return false;
		
		Hashtable<Integer, Tag<Material>> tagBlacklist = new Hashtable<>();
		
		tagBlacklist.put(1, Tag.ENDERMAN_HOLDABLE);
		tagBlacklist.put(2, Tag.BAMBOO_PLANTABLE_ON);
		tagBlacklist.put(4, Tag.SNOW);

		Hashtable<Material, Integer> materialHashMap = new Hashtable<>();
		Iterator<Material> materials = Arrays.stream(Material.values()).iterator();
		
		int i = 0;
		while(materialHashMap.size() < 256 && materials.hasNext()) {
			Material material = materials.next();
			if(
				material.isSolid() && !material.hasGravity() && 
				!material.isInteractable() && !material.equals(Material.FARMLAND) &&
				!this.isTagged(tagBlacklist, material)
			) {
				materialHashMap.put(material, i);
				i++;
			}
		}
		
		List<Integer> fileBytes = new ArrayList<Integer>();
		int row = 0;
		try {
			System.out.println("Starting read");
			while(true) {
				for(int x = 0; x < BLOCKLEN * CHUNKSIZE; x++) {
					for(int y = 0; y < CHUNKHEIGHT; y++) {
						for(int z = 0; z < CHUNKSIZE; z++) {
							if(fileBytes.size() >= Integer.parseInt(args[1])) {
								System.out.println("Starting write");
								try {
									Writer wr = new FileWriter(args[0], true);
									for(Integer b : fileBytes) {
										wr.write(b.toString() + ",");
									}
									wr.close();
								} catch (IOException e) {
								    e.printStackTrace();
								}
								return true;
							}
							Block b = ((Player)sender).getWorld().getBlockAt(
								Integer.parseInt(args[2])+x, CHUNKHEIGHT-y, Integer.parseInt(args[4])+(CHUNKSIZE*row)+z);
							fileBytes.add(materialHashMap.get(Material.getMaterial(b.getType().name())));
						}
					}
				}
				row++;
			}
		} catch (Exception e) {
			// Triggers error when trying to write outside currently rendered area.
			e.printStackTrace();
			return true;
		}
	}
	
	private boolean isTagged(Hashtable<Integer, Tag<Material>> blacklist, Material material) {
		Enumeration<Integer> e = blacklist.keys();
		while (e.hasMoreElements()) {
			int key = e.nextElement();
			if(blacklist.get(key).isTagged(material)) return true;
		}
		return false;
	}
}
```

```python
f = open('/tmp/blocks', 'r').read()
f = f.split(',')[:-1]

for i in range(len(f)):
    f[i] = int(f[i]).to_bytes(1, 'big')

fs = open('./out', 'wb')
fs.write(b''.join(f))
fs.close()
```

After recovering the original file. It can be seen that it is an ext4 file system. Mounting the file system gives the flag.

Flag: `gigem{r3curs1v3_f1l3_st0rag3}`
