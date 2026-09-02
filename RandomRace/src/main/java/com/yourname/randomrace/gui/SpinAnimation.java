package com.yourname.randomrace.gui;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.managers.AssignmentManager;
import com.yourname.randomrace.utils.MessageUtil;
import com.yourname.randomrace.utils.SoundUtil;
import me.athlaeos.valhallaraces.Race;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.Sound;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.HandlerList;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryCloseEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemStack;
import org.bukkit.scheduler.BukkitTask;

import java.util.ArrayList;
import java.util.List;

public class SpinAnimation implements Listener {
    private static final int SLOTS = 9;
    private static final int CENTER = 4;

    private static final int[][] PHASES = {
        {2, 20},
        {4, 10},
        {8, 5}
    };
    private static final int TOTAL_CYCLES;
    static {
        int t = 0;
        for (int[] p : PHASES) t += p[1];
        TOTAL_CYCLES = t;
    }

    private final RandomRacePlugin plugin;
    private final Player player;
    private final Race winner;
    private final AssignmentManager assignmentManager = new AssignmentManager();
    private final List<Race> reel;
    private Inventory inventory;
    private BukkitTask task;
    private int tickCount = 0;

    public SpinAnimation(RandomRacePlugin plugin, Player player, Race winner) {
        this.plugin = plugin;
        this.player = player;
        this.winner = winner;
        this.reel = buildReel();
    }

    private List<Race> buildReel() {
        List<Race> candidates = new ArrayList<>(plugin.getRacePoolManager().getAvailableRaces(player));
        if (candidates.isEmpty()) candidates.add(winner);
        int totalItems = TOTAL_CYCLES + SLOTS;
        List<Race> reel = new ArrayList<>(totalItems);
        for (int i = 0; i < totalItems; i++) {
            if (i == TOTAL_CYCLES + CENTER) {
                reel.add(winner);
            } else {
                reel.add(candidates.get(i % candidates.size()));
            }
        }
        return reel;
    }

    public void start() {
        inventory = plugin.getServer().createInventory(null, SLOTS, MessageUtil.color("&8Random Race"));
        Bukkit.getPluginManager().registerEvents(this, plugin);
        player.openInventory(inventory);
        SoundUtil.play(player, Sound.BLOCK_CHEST_OPEN);
        task = plugin.getServer().getScheduler().runTaskTimer(plugin, () -> {
            step();
            tickCount++;
            if (tickCount >= TOTAL_CYCLES + 1) {
                task.cancel();
                finish();
            }
        }, 10L, 2L);
    }

    private void step() {
        for (int slot = 0; slot < SLOTS; slot++) {
            int idx = tickCount + slot;
            Race r = reel.get(idx % reel.size());
            inventory.setItem(slot, new ItemStack(plugin.getRacePoolManager().materialFor(r), 1));
        }
        SoundUtil.play(player, Sound.UI_BUTTON_CLICK);
    }

    private void finish() {
        HandlerList.unregisterAll(this);
        SoundUtil.play(player, Sound.BLOCK_NOTE_BLOCK_PLING);
        plugin.getServer().getScheduler().runTaskLater(plugin, () -> {
            player.closeInventory();
            assignmentManager.assign(player, winner);
            plugin.getPlayerDataManager().markClaimed(player.getUniqueId());
            String name = stripColor(winner.getDisplayName());
            String assigned = MessageUtil.replace("{race}", name,
                    plugin.getConfig().getString("messages.race-assigned", "&aYou have been chosen as a &e{race}&a!"));
            player.sendMessage(MessageUtil.color(assigned));
            SoundUtil.play(player, Sound.ENTITY_FIREWORK_ROCKET_BLAST);
            if (plugin.getConfig().getBoolean("broadcast-enabled", true)) {
                String bc = MessageUtil.replace("{player}", player.getName(),
                        MessageUtil.replace("{race}", name,
                                plugin.getConfig().getString("messages.broadcast", "&e{player} &ahas been destined to be a &e{race}&a!")));
                Bukkit.broadcastMessage(MessageUtil.color(bc));
            }
        }, 40L);
    }

    private String stripColor(String s) {
        if (s == null) return "";
        return s.replaceAll("(?i)\\u00A7[0-9a-fk-or]", "");
    }

    @EventHandler
    public void onClose(InventoryCloseEvent e) {
        if (e.getPlayer().getUniqueId().equals(player.getUniqueId())) {
            if (task != null) task.cancel();
            HandlerList.unregisterAll(this);
        }
    }

    @EventHandler
    public void onClick(InventoryClickEvent e) {
        if (e.getWhoClicked().getUniqueId().equals(player.getUniqueId())) {
            e.setCancelled(true);
        }
    }
}
