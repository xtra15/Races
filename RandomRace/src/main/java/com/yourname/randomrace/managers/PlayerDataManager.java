package com.yourname.randomrace.managers;

import com.yourname.randomrace.RandomRacePlugin;
import org.bukkit.configuration.file.YamlConfiguration;

import java.io.File;
import java.io.IOException;
import java.util.UUID;

public class PlayerDataManager {
    private final RandomRacePlugin plugin;
    private final File file;
    private YamlConfiguration data;

    public PlayerDataManager(RandomRacePlugin plugin) {
        this.plugin = plugin;
        this.file = new File(plugin.getDataFolder(), "playerdata.yml");
        if (!file.exists()) {
            plugin.saveResource("playerdata.yml", false);
        }
        this.data = YamlConfiguration.loadConfiguration(file);
    }

    public boolean hasClaimed(UUID uuid) {
        return data.getLong(uuid + ".claimed", 0L) > 0L;
    }

    public void markClaimed(UUID uuid) {
        data.set(uuid + ".claimed", System.currentTimeMillis());
        save();
    }

    public void clear(UUID uuid) {
        data.set(uuid.toString(), null);
        save();
    }

    private void save() {
        try {
            data.save(file);
        } catch (IOException e) {
            plugin.getLogger().warning("Could not save playerdata.yml: " + e.getMessage());
        }
    }
}
